
# Importazione
import os, sys, json, shutil
from datetime import datetime

# Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazione Whoosh per la gestione dell'indicizzazione e della ricerca
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED, KEYWORD, DATETIME
from whoosh.qparser import QueryParser, GtLtPlugin
from whoosh.query import Wildcard, DateRange, Term, Phrase, And, Or, Not
from whoosh import index

# Importazione moduli di progetto
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# ################################################## #

class MyWhoosh:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "indexes", "whoosh_indexes")
    DATASET_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "dataset", "dataset.json")
    
    # ################################################## #

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyWhoosh.DATASET_FILE_PATH):
            raise FileNotFoundError(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyWhoosh.DATASET_FILE_PATH}\'.")
        
        # Controllo se la cartella degli indici esiste
        if os.path.exists(MyWhoosh.INDEX_DIRECTORY_PATH):
            # Se esiste la elimino
            shutil.rmtree(MyWhoosh.INDEX_DIRECTORY_PATH)
        
        # Creazione della cartella degli indici
        if not os.path.exists(MyWhoosh.INDEX_DIRECTORY_PATH):
            os.mkdir(MyWhoosh.INDEX_DIRECTORY_PATH)

    @staticmethod
    def _write_indexes():
        """ Funzione che scrive gli indici per la ricerca. """
        
        # Apertura file dataset
        with open(MyWhoosh.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f) # Caricamento documenti formato JSON

        # SCHEMA DELL'INDICE
        SCHEMA = Schema(
            
            # Campi memorizzati
            number    = ID(stored=True, unique=True),   # Numero identificativo del documento
            title     = TEXT(stored=True),              # Titolo del documento
            authors   = KEYWORD(stored=True),           # Autori del documento
            date      = DATETIME(stored=True),          # Data di pubblicazione
            status    = KEYWORD(stored=True),           # Stato del documento
            abstract  = TEXT(stored=True),              # Abstract del documento
            keywords  = TEXT(stored=True),              # Parole chiave del documento
            more_info = STORED,                         # Altre informazioni memorizzabili
            files     = STORED,                         # Files associati al documento
            
            # Campi non memorizzati
            content   = TEXT                            # Contenuto del documento
        )

        # Creazione writer per aggiungere documenti all'indice
        writer = index.create_in(MyWhoosh.INDEX_DIRECTORY_PATH, SCHEMA).writer()

        # Definizione della barra di caricamento che viene visualizzata durante l'esecuzione
        with alive_bar(len(documents), title="Indicizzazione dei documenti con Whoosh", spinner="waves", bar=_bar) as bar:
            
            # Inserire documenti nell'indice
            for doc in documents:
                
                bar() # Avanza la barra
                
                # Parsing della data (data di oggi se fallisce)
                try: date = datetime.strptime(doc["Date"], "%Y-%m")
                except Exception: date = datetime.today()

                # Aggiunta del documento
                writer.add_document(
                    
                    # Campi memorizzati
                    number    = doc["Number"],                 # Identificativo del documento
                    title     = doc["Title"],                  # Titolo
                    authors   = doc["Authors"],                # Autori
                    date      = date,                          # Data di pubblicazione
                    status    = doc["Status"],                 # Stato
                    abstract  = doc["Abstract"],               # Abstract
                    keywords  = doc["Keywords"],               # Parole chiave
                    more_info = doc["More Info"],              # Altre informazioni
                    files     = doc["Files"],                  # Files
                    
                    # Campi non memorizzati
                    content   = doc["Content"]                 # Contenuto
                )

        # Commit
        writer.commit()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        logging.debug("Whoosh: Indicizzazione dei documenti...")
        MyWhoosh._prepare_folders_and_files()
        MyWhoosh._write_indexes()

    # ################################################## #

    @staticmethod
    def _results_to_json(results):
        """Converte i risultati in un formato JSON."""
        
        results_list = []
        
        for result in results:
            
            result_dict = dict(result)

            # Converte datetime in stringhe
            for key, value in result_dict.items():
                if isinstance(value, datetime):
                    result_dict[key] = value.strftime('%Y-%m')

            results_list.append(result_dict)
        
        return results_list

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        ################################
        ## INIZIALIZZAZIONE PARAMETRI ##
        ################################

        # Verifica se la cartella degli indici esiste
        if not os.path.exists(MyWhoosh.INDEX_DIRECTORY_PATH):
            # Altrimenti crea gli indici
            MyWhoosh.create_indexes()

        # Apertura dell'indice esistente
        ix = index.open_dir(MyWhoosh.INDEX_DIRECTORY_PATH)

        ############################################################
        ## QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO ##
        ############################################################

        # Parsing della query principale sul campo "content"
        content_query = QueryParser("content", ix.schema).parse(
            data["ricerca_principale"].lower() # case-insensitive
        )

        ###########################################################################
        ## RICERCA SU PIU' CAMPI - CREAZIONE DELLE QUERIES PER TERMINI SECONDARI ##
        ###########################################################################
        
        # Inizializzazione delle liste per gli operatori logici
        and_terms, not_terms, or_terms = [], [], []

        # Elenco dei termini da cercare
        for term_data in data["terms"]:
            
            # Estrazione dei valori del termine
            term = term_data["term"].lower()
            operator = term_data["operator"].strip().upper()
            field = term_data["field"].strip().upper()

            # Mappatura dei campi del documento
            field_mapping = {
                "TITLE": "title",
                "DESCRIPTION": "abstract",
                "KEYWORDS": "keywords",
                "AUTHORS": "authors"
            }
            
            # Recupero del campo ("abstract" di default)
            field = field_mapping.get(field, "abstract")

            # Mappatura tra operatori e liste dei termini
            operator_mapping = {
                "AND": and_terms,
                "NOT": not_terms,
                "OR": or_terms
            }
            
            # Termine aggiunto alla lista in base all'operatore
            operator_mapping.get(operator, "AND").append(Term(field, term))

        # Creazione delle query se le liste non sono vuote
        and_query = And(and_terms) if and_terms else None
        not_query = Not(Or(not_terms)) if not_terms else None
        or_query = Or(or_terms) if or_terms else None

        # Combina le query valide in un'unica query composta
        query_parts = [q for q in [and_query, not_query, or_query] if q]
        terms_query = And(query_parts) if query_parts else None

        ###########################################################################
        ## RICERCA PER STATO - CREAZIONE DI UNA QUERY PER LO STATO DEI DOCUMENTI ##
        ###########################################################################

        # Query dello stato
        status_query = None
        
        # Verifica se almeno uno degli stati da cercare è stato selezionato
        should_search_for_status = any(data.get(key) for key in [
            "standard_track", "best_current_practice", "informational", "experimental", "historic"
        ])

        if should_search_for_status:
            
            # Lista degli stati
            status_filters = []

            status_mapping = {
                "best_current_practice": "Best",         # Best Current Practice
                "informational": "Informational",        # Informational
                "experimental": "Experimental",          # Experimental
                "historic": "Historic",                  # Historic
            }

            # Aggiungi filtro per "standard_track" se presente
            if data.get("standard_track"):
                
                standard_track_value = data.get("standard_track_value", "").strip().upper()
                
                standard_track_mapping = {
                    "PROPOSED_STANDARD": "Proposed",      # Proposed Standard
                    "DRAFT_STANDARD": "Draft",            # Draft Standard
                    "INTERNET_STANDARD": "Internet",      # Internet Standard
                }

                # Aggiungi il filtro per lo stato se valido
                if standard_track_value in standard_track_mapping:
                    status_filters.append(Wildcard('status', f"*{standard_track_mapping[standard_track_value]}*"))

            # Aggiungi filtri per gli altri stati
            for key, status in status_mapping.items():
                if data.get(key):  # Verifica se lo stato è selezionato
                    status_filters.append(Wildcard('status', f"*{status}*"))

            # Se ci sono filtri
            if status_filters:
                # Crea la query composta OR
                status_query = Or(status_filters)
        
        ############################################################################
        ## RICERCA PER DATA - CREAZIONE DI UNA QUERY PER IL FILTRAGGIO SULLE DATE ##
        ############################################################################

        date_query = None  # Valore di default per la date query
        date_filter = data.get("dates", "").strip().upper() # Opzione selezionata

        # Se l'opzione selezionata è "ALL_DATES", non filtriamo
        if date_filter != "ALL_DATES":
            
            # Filtro per anno specifico (SPECIFIC_YEAR)
            if date_filter == "SPECIFIC_YEAR" and data["date_year"]:
                
                specific_year_int = data.get("date_year")

                if specific_year_int:
                    try:
                        # Calcolo primo e ultimo giorno dell'anno
                        from_specific_year = datetime(specific_year_int, 1, 1)
                        to_specific_year = datetime(specific_year_int, 12, 31)

                        # Crea la query per l'intervallo dell'anno specifico
                        date_query = DateRange("date", from_specific_year, to_specific_year)
                    except ValueError: pass

            # Filtro per intervallo tra date (DATE_RANGE)
            elif date_filter == "DATE_RANGE" and data["date_from_date"] and data["date_to_date"]:
                
                from_date_str = data.get("date_from_date")
                to_date_str = data.get("date_to_date")

                if from_date_str and to_date_str:
                    try:
                        # Parsing delle date (mese/anno)
                        from_date = datetime.strptime(from_date_str.strip(), "%Y-%m")
                        to_date = datetime.strptime(to_date_str.strip(), "%Y-%m")

                        # Crea la query per l'intervallo di date
                        date_query = DateRange("date", from_date, to_date)
                    except ValueError: pass

        ###########################################################################
        ## COSTRUZIONE DELLA QUERY FINALE - COMBINAZIONE DELLE QUERY INDIVIDUALI ##
        ###########################################################################

        # Filtra le parti della query che non sono valide (uguali a None)
        combined_query_parts = [q for q in [content_query, terms_query, status_query, date_query] if q]

        # Combina le query valide con un operatore "AND"
        combined_query = And(combined_query_parts) if combined_query_parts else None

        #######################################################################################
        ## ESTRAZIONE DEI RISULTATI - ESECUZIONE DELLA RICERCA E FORMATTAZIONE DEI RISULTATI ##
        #######################################################################################

        # Apre il searcher
        with ix.searcher() as searcher:
            
            # Esegue la ricerca
            results = searcher.search(combined_query, limit=data.get("size"))

            # Converte i risultati in formato JSON
            results = MyWhoosh._results_to_json(results)
        
        # Restituzione
        return results
        
        # ########################################################### #

    @staticmethod
    def process(query: dict):
        return MyWhoosh._execute_query(query)

# ################################################## #

if __name__ == "__main__":
    MyWhoosh._prepare_folders_and_files()