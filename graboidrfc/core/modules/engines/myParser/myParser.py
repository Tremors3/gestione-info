
# Altri Imports
import requests
import os, re, json
from time import sleep
import concurrent.futures # Per ThreadPool
from bs4 import BeautifulSoup # BeautifulSoup per parsing
from typing import Optional, Generator, List, Dict

# Per barre di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Import Moduli Progetto
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

class MyParser:

    # %%%%%% PATHS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    
    # DATASET DIRECTORY PATHS
    DATASET_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "dataset", "dataset.json")
    
    # SETTINGS FILE PATHS
    SETTINGS_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "config", "parser.json")
    
    # %%%%%% CLASS VARS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    TOTAL_RFC_NUMBER = 9688  # Numero totale di documenti disponibili

    URL = { # LINKS & URLS 
        "URL_METADATA" : "https://www.rfc-editor.org/search/rfc_search_detail.php?page=All&pubstatus[]=Any&pub_date_type=any&abstract=abson&keywords=keyson&sortkey=Number&sorting=ASC",
        "URL_PREFIX"  : "https://www.rfc-editor.org/rfc/rfc",
        "URL_POSTFIX" : ".html"
    }

    STATUSES = (
        "Proposed Standard", "Draft Standard", "Internet Standard",     # Standard Track
        "Best Current Practice",
        "Informational",
        "Experimental",
        "Historic",
        "Unknown",
        "Not Issued"
    )
    
    MONTHS = {
        "January"  : "01",
        "February" : "02",
        "March"    : "03",
        "April"    : "04",
        "May"      : "05",
        "June"     : "06",
        "July"     : "07",
        "August"   : "08",
        "September": "09",
        "October"  : "10",
        "November" : "11",
        "December" : "12",
    }

    # %%%%%% PAGES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def _download_page(url: str, session: requests.Session, timeout: int, delay_ms: int) -> Optional[str]:
        """
        Scarica una singola pagina da un URL specificato.
        """
        try:
            sleep(delay_ms / 1000.0) # Delay
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            # Log Rimosso perchè duplica la barra di caricamento
            #logging.warning(f"Errore durante il download della pagina: {e}")
            return None

    @staticmethod
    def _parse_page(html_content: str) -> Optional[Dict]:
        """
        Effettua il parsing del contenuto HTML in un dizionario.
        """
        try:
            # Analizzatore del contenuto del documento
            soup = BeautifulSoup(html_content, 'html.parser')

            # TODO: Rimozione header del documento. (Tramite rejex?)

            # Formatta il testo su una singola linea
            text = soup.get_text().strip().replace('\n', ' ')
            # Rimozione del padding (. . . . . . . exc...) dell'indice
            text = re.sub(r'(\. \.)(?=\s)', '', text)
            # Sostituisci spazi ripetuti con uno spazio singolo
            text = re.sub(r' +', ' ', text)
            
            # Restituzione del contenuto delstuale riformattato
            return text
        except Exception as e:
            logging.warning(f"Errore durante il parsing del contenuto HTML: {e}")
            return None

    @staticmethod
    def _task(meta: dict, session: requests.Session, timeout: int, delay_ms: int) -> Optional[Dict]:
        """
        Scarica e parsifica una pagina specificata.
        """
        # Costruzione dello URI della pagina
        url = MyParser.URL["URL_PREFIX"] + meta['Number'] + MyParser.URL["URL_POSTFIX"]
        
        # Scaricamento del contenuto della pagina
        html_content = MyParser._download_page(url, session, timeout, delay_ms)
        if html_content is None:
            return None
        
        # Estendiamo i metadati della pagina con il corpo parsato del documento
        meta["Content"] = MyParser._parse_page(html_content)
        
        # Restituiamo i metadati (con tanto di corpo del documento)
        return meta

    @staticmethod
    def _download_and_parse_pages(metadata: List[dict], workers: int = 10, timeout: int = 10, delay_ms: int = 50) -> Generator[Dict, None, None]:
        """
        Scarica e parsifica più pagine in parallelo.
        """
        # Apertura di una sessione http e di una ThreadPool
        with requests.Session() as session, concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

            # Creazione delle task per la Threadpool
            futures = {
                executor.submit(MyParser._task, meta, session, timeout, delay_ms): meta for meta in metadata
            }
            
            # Imposta il totale per la percentuale
            # pbar = tqdm(total=len(futures), ascii="•Cc=")
            with alive_bar(len(futures), title=f"Parsing dei documenti", spinner="waves", bar=_bar) as b:
            
                # Restituzione dei metadati che adesso contengono il corpo completo del documento
                for future in concurrent.futures.as_completed(futures):
                    
                    # Incrementa di uno i documenti scaricati
                    b()
                    
                    # Restituzione del contenuto parsato
                    # della pagina e i relativi metadati
                    try:
                        page = future.result()
                        if page is not None:
                            yield page
                    except Exception as e:
                        logging.warning(f"Errore durante l'elaborazione di un task: {e}")

    # %%%%%% METADATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def _download_and_parse_metadata(index_begin: int, index_end: int) -> Optional[dict]:
        """
        Scarica e analizza i metadati di tutti gli RFC specificati.
        """
        # Apertura di una sessione http
        with requests.Session() as session:
            try:
                # Effettuazione la richiesta alla pagina
                response = session.get(MyParser.URL["URL_METADATA"])
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.error(f"Errore durante il download dei metadati: {e}")
                return None

            # Analizzatore del contenuto del documento
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ricava la tabella contenente i metadati
            table = soup.find("table", {"class": "gridtable"})
            if not table:
                logging.error("Tabella dei metadati non trovata.")
                return None

            # Estrae una lista contenente tutte le righe della tabella
            rows = table.find_all("tr")[(index_begin * 3) - 2:(index_end * 3)+1]
            
            # Parsa le righe della tabella in un json
            return MyParser._parse_rows(rows)

    @staticmethod
    def _parse_rows(rows: list[any]) -> Optional[dict]:
        """
        Analizza un insieme di righe HTML e ne estrae i metadati.
        """
        parsed_data = []

        # Itera attraverso tre righe alla volta
        # group[0] --> Metadati dell'RFC
        # group[1] --> Estratto dell'RFC
        # group[2] --> Keywords dell'RFC
        with alive_bar(len(rows) // 3, title=f"Parsing dei metadati", spinner="waves", bar=_bar) as b:
            for i in range(0, len(rows), 3):
                group = rows[i:i + 3]

                # Parsa il gruppo di righe in un json
                parsed = MyParser._parse_group(group)
                if parsed:
                    parsed_data.append(parsed)
                
                b() # Avanza barra di caricamento
                    
        # Restituisce l'elenco di gruppi parsati
        return parsed_data

    @staticmethod
    def _parse_group(group: list[any]) -> Optional[dict]:
        """
        Analizza un gruppo di righe (metadati, abstract, keywords).
        """
        try:
            # Ricordiamo che:
            # group[0] --> Metadati dell'RFC
            # group[1] --> Estratto dell'RFC
            # group[2] --> Keywords dell'RFC
            
            # Metadati
            element = group[0].find_all("td")
            
            # Ottenimento dello stato
            text = element[6].get_text().replace('\u00a0', ' ').strip()
            status = next((s for s in MyParser.STATUSES if s in text), "")
            
            # Non consideriamo gli rfc non pubblicati
            if status == "Not Issued": return None
            
            # Formattazione della data
            date = element[4].get_text().replace('\u00a0', ' ').split(' ')
            if len(date) > 2: date = date[1::] # Non consideriamo il giorno
            date[0] = MyParser.MONTHS[date[0]] # Tradiciamo il mese in numero
            date = "-".join(date[::-1]) # Ricostruiamo la data: YYYY-MM
            
            # Costruzione dei metadati
            current = {
                "Number": element[0].get_text().split('\u00a0')[1].split(' ')[0].strip(),
                "Files": [tf.strip().lower().replace("text", "txt") for tf in element[1].get_text().replace('\u00a0', ' ').split(',') if tf.strip() in ['HTML', 'TEXT', 'XML', 'PDF']],
                "Title": element[2].get_text().replace('\u00a0', ' ').strip(),
                "Authors": [au.strip() for au in element[3].get_text().replace('\u00a0', ' ').split(',')],
                "Date": date,
                "More Info": element[5].get_text().replace('\u00a0', ' ').strip(),
                "Status": status
            }

            # Abstract
            current["Abstract"] = MyParser._parse_optional_row(group, 1, False)

            # Keywords
            current["Keywords"] = MyParser._parse_optional_row(group, 2, True)

            return current
        except (IndexError, AttributeError) as e:
            logging.warning(f"Errore durante il parsing del gruppo: {e}")
            return None

    @staticmethod
    def _parse_optional_row(group, index: int, to_list: bool) -> list[str] | str:
        """
        Analizza una riga opzionale (Abstract o Keywords).
        """
        if len(group) > index:
            row = group[index].find_all("td")
            if len(row) > 1:
                if (to_list):
                    # Keywords MyParser
                    return [item.strip() for item in row[1].get_text().split(',') if len(item) > 1]
                else:
                    # Abstract MyParser
                    return row[1].get_text().replace('\n',' ').replace('\r', '').strip()
        return ""

    # %%%%%% GETTING SETTINGS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def __get_settings(fp:str=None):
        """Funzione che legge e restutiusce le impostazioni in formato JSON."""
        
        # Ottenimento del percorso del file delle impostazioni
        FILE_PATH = fp if fp else __class__.SETTINGS_FILE_PATH
        
        # Controllo se il file delle impostazioni esiste
        if not os.path.isfile(FILE_PATH):
            raise FileNotFoundError(f"Il file del dataset non è stato trovato al seguente percorso: \'{FILE_PATH}\'.")

        # Lettura e restituzione delle impostazioni in formato JSON
        with open(FILE_PATH, mode="r", encoding='utf-8') as f:
            return json.load(f)

    # %%%%%% GENERATE DATASET %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def generate_dataset(output_file: str = None) -> None:
        """Genera un dataset scaricando e parsificando le pagine specificate."""
        
        # Lettura delle impostazioni
        settings = __class__.__get_settings()
        
        # Impostazione primo indice
        index_begin = settings["DOCUMENTS"]["BEGIN_INDEX"]
        index_begin = index_begin if index_begin >= 1 and index_begin <= MyParser.TOTAL_RFC_NUMBER else 1
        
        # Impostazione secondo indice
        index_end = settings["DOCUMENTS"]["END_INDEX"]
        index_end = index_end if index_end >= 1 and index_end <= MyParser.TOTAL_RFC_NUMBER else MyParser.TOTAL_RFC_NUMBER
        
        # Verifica correttezza indici
        if index_begin > index_end:
            index_end = index_begin
        
        # impostazione parametri threadpool
        workers, timeout, delay_ms = settings["DOWNLOAD"]["WORKERS"], settings["DOWNLOAD"]["TIMEOUT"], settings["DOWNLOAD"]["DELAY_MS"]
        
        # Impostazione output file
        output_file = output_file if output_file is not None else MyParser.DATASET_FILE_PATH
        
        # Scaricamento e parsing dei metadati
        logging.debug(f"Download e Parsing dei Metadati...")
        metadata = MyParser._download_and_parse_metadata(index_begin, index_end)
        
        # Scaricamento e parsing del corpo dei documenti
        logging.debug(f"Download e Parsing dei Documenti...")
        page_list = []
        for page in MyParser._download_and_parse_pages(metadata, workers, timeout, delay_ms):
            page_list.append(page)

        # Salvataggio del dataset nel file
        logging.debug(f"Scrivendo su file...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(page_list, f, ensure_ascii=False, indent=4)
        logging.info(f"dataset salvato in \"{output_file}\".")

def start():
    MyParser.generate_dataset()

# UNIT TESTING
if __name__ == "__main__":
    start()