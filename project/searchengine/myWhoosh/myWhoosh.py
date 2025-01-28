
# Importazioni standard
import os, sys, json, shutil
from datetime import datetime

# Importazioni Whoosh per la gestione dell'indicizzazione e della ricerca
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED, KEYWORD, DATETIME
from whoosh.qparser import QueryParser, GtLtPlugin
from whoosh.query import Wildcard, DateRange, Term, Phrase, And, Or, Not
from whoosh import index

# Importazione del logger personalizzato del progetto
from project.searchengine.myLogger.myLogger import logger as logging, bcolors

# ################################################## #

class MyWhoosh:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(CURRENT_FILE_PATH, "indexes_dir")
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    
    # ################################################## #

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyWhoosh.DATASET_FILE_PATH):
            logging.error(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyWhoosh.DATASET_FILE_PATH}\'.")
            sys.exit(1)
        
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
        
        # Apro il file del dataset in modalità lettura con codifica UTF-8
        with open(MyWhoosh.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f) # Carico i documenti in formato JSON

        # Definisco lo schema per l'indice
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

        # Crea un writer per aggiungere documenti all'indice
        writer = index.create_in(MyWhoosh.INDEX_DIRECTORY_PATH, SCHEMA).writer()

        # Ciclo sui documenti e li aggiungo all'indice
        for doc in documents:
            
            # Provo a fare il parsing della data, se fallisce prendo la data di oggi
            try: date = datetime.strptime(doc["Date"], "%Y-%m")
            except Exception:
                date = datetime.today()

            # Aggiungo un documento all'indice con i vari campi
            writer.add_document(
                
                # Campi memorizzati
                number    = doc["Number"],                 # Numero identificativo del documento
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

        # Commetto i cambiamenti effettuati nel writer, rendendo permanenti gli indici
        writer.commit()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        MyWhoosh._prepare_folders_and_files()
        MyWhoosh._write_indexes()

    # ################################################## #

    @staticmethod
    def _results_to_json(results):
        """Converte i risultati di Whoosh in un formato JSON-friendly."""
        
        results_list = []
        
        for result in results:
            
            result_dict = dict(result)

            # Converte datetime in stringhe
            for key, value in result_dict.items():
                if isinstance(value, datetime):
                    result_dict[key] = value.strftime('%Y-%m')  # Formatta come stringa

            results_list.append(result_dict)
        
        return json.dumps(results_list)

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # ########################################################### #
        # INIZIALIZZAZIONE PARAMETRI
        # ########################################################### #

        # Verifica se la cartella degli indici esiste, altrimenti crea gli indici
        if not os.path.exists(MyWhoosh.INDEX_DIRECTORY_PATH):
            MyWhoosh.create_indexes()

        # Apertura dell'indice esistente
        ix = index.open_dir(MyWhoosh.INDEX_DIRECTORY_PATH)

        # ########################################################### #
        # QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO
        # ########################################################### #

        # Parsing della query principale sul campo "content" con la ricerca case-insensitive
        content_query = QueryParser("content", ix.schema).parse(
            data["ricerca_principale"].lower()
        )

        # ########################################################### #
        # RICERCA SU PIU' CAMPI - CREAZIONE DI UNA QUERY BOOLEANA COMBINATA
        # ########################################################### #
        
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
            
            # Se il campo non è trovato, assegna "abstract" come campo di default
            field = field_mapping.get(field, "abstract")

            # Mappatura tra operatori logici e liste dei termini
            operator_mapping = {
                "AND": and_terms,
                "NOT": not_terms,
                "OR": or_terms
            }
            
            # Aggiungi il termine alla lista appropriata in base all'operatore
            operator_mapping.get(operator, "AND").append(Term(field, term))

        # Creazione delle query solo se le liste non sono vuote
        and_query = And(and_terms) if and_terms else None
        not_query = Not(Or(not_terms)) if not_terms else None
        or_query = Or(or_terms) if or_terms else None

        # Combina le query valide in un'unica query complessa
        query_parts = [q for q in [and_query, not_query, or_query] if q]
        terms_query = And(query_parts) if query_parts else None

        # ########################################################### #
        # RICERCA PER STATO - CREAZIONE DI UNA QUERY PER LO STATO DEI DOCUMENTI
        # ########################################################### #

        status_query = None  # Valore di default per la query dello stato

        # Verifica se almeno uno degli stati da cercare è stato selezionato
        should_search_for_status = any(data.get(key) for key in [
            "standard_track", "best_current_practice", "informational", "experimental", "historic"
        ])

        if should_search_for_status:
            
            status_filters = []  # Lista per raccogliere i filtri di stato

            # Mappatura tra chiavi dei dati e i relativi stati
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

                # Aggiungi il filtro per lo stato specifico se valido
                if standard_track_value in standard_track_mapping:
                    status_filters.append(Wildcard('status', f"*{standard_track_mapping[standard_track_value]}*"))

            # Aggiungi filtri per gli altri stati
            for key, status in status_mapping.items():
                if data.get(key):  # Verifica se lo stato è selezionato
                    status_filters.append(Wildcard('status', f"*{status}*"))

            # Se ci sono filtri, crea la query combinata OR
            if status_filters:
                status_query = Or(status_filters)
        
        # ########################################################### #
        # RICERCA PER DATA - CREAZIONE DI UNA QUERY PER IL FILTRAGGIO SULLE DATE
        # ########################################################### #

        date_query = None  # Valore di default per la query della data
        date_filter = data.get("dates", "").strip().upper() # Opzione selezionata

        # Se l'opzione selezionata è "ALL_DATES", non filtriamo per data
        if date_filter != "ALL_DATES":
            
            # Filtro per un anno specifico (SPECIFIC_YEAR)
            if date_filter == "SPECIFIC_YEAR" and data["date_year"]:
                
                specific_year_int = data.get("date_year", 2000)

                if specific_year_int:
                    try:
                        # Calcolo primo e ultimo giorno dell'anno
                        from_specific_year = datetime(specific_year_int, 1, 1)
                        to_specific_year = datetime(specific_year_int, 12, 31)

                        # Crea la query per l'intervallo dell'anno specifico
                        date_query = DateRange("date", from_specific_year, to_specific_year)
                    except ValueError:
                        pass  # In caso di errore nel parsing, non fare nulla

            # Filtro per intervallo di date (DATE_RANGE)
            elif date_filter == "DATE_RANGE" and data["date_from_date"] and data["date_to_date"]:
                
                from_date_str = data.get("date_from_date", "").strip()
                to_date_str = data.get("date_to_date", "").strip()

                if from_date_str and to_date_str:
                    try:
                        # Parsing delle date (mese/anno)
                        from_date = datetime.strptime(from_date_str, "%Y-%m")
                        to_date = datetime.strptime(to_date_str, "%Y-%m")

                        # Crea la query per l'intervallo di date
                        date_query = DateRange("date", from_date, to_date)
                    except ValueError:
                        pass  # In caso di errore nel parsing, non fare nulla

        # ########################################################### #
        # COSTRUZIONE DELLA QUERY FINALE - COMBINAZIONE DELLE QUERY INDIVIDUALI
        # ########################################################### #

        # Filtra le parti della query che sono valide (non None)
        combined_query_parts = [q for q in [content_query, terms_query, status_query, date_query] if q]

        # Combina le query valide con un operatore "AND" (e.g., tutte le condizioni devono essere soddisfatte)
        combined_query = And(combined_query_parts) if combined_query_parts else None

        # ########################################################### #
        # ESTRAZIONE DEI RISULTATI - ESECUZIONE DELLA RICERCA E FORMATTAZIONE DEI RISULTATI
        # ########################################################### #

        # Apre un "searcher" per eseguire la ricerca sugli indici
        with ix.searcher() as searcher:
            
            # Esegue la ricerca utilizzando la query combinata e un limite sui risultati (size)
            results = searcher.search(combined_query, limit=data.get("size"))

            # Converte i risultati in formato JSON-friendly
            results = MyWhoosh._results_to_json(results)
        
        # ########################################################### #
        
        # Restituisce i risultati formattati
        return results
    
    # ################################################## #
    
    @staticmethod
    def process(query: dict):
        return MyWhoosh._execute_query(query)

# ################################################## #

if __name__ == "__main__":
    MyWhoosh._prepare_folders_and_files()