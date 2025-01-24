import os, sys, json, shutil

# #################################################################################################### #

from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED, KEYWORD, DATETIME
from whoosh.qparser import QueryParser, GtLtPlugin

# #################################################################################################### #

from project.searchengine.myLogger.myLogger import logger as logging, bcolors

# #################################################################################################### #

class MyWhoosh:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(CURRENT_FILE_PATH, "indexes")
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    
    # #################################################################################################### #

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
        
        # Apertura del file del dataset
        with open(MyWhoosh.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)

        # Schema per l'indice
        SCHEMA = Schema(
            number    = ID(stored=True, unique=True),
            files     = STORED,
            title     = TEXT(stored=True),
            authors   = TEXT(stored=True),
            date      = STORED,
            more_info = STORED,
            status    = TEXT(stored=True),
            abstract  = TEXT(stored=True),
            keywords  = KEYWORD(commas=True),
            content   = TEXT
        )
        
        writer = index.create_in(MyWhoosh.INDEX_DIRECTORY_PATH, SCHEMA).writer()

        # Scrittura degli indici
        for doc in documents:
            writer.add_document(
                number    = doc["Number"],
                files     = doc["Files"],
                title     = doc["Title"],
                authors   = doc["Authors"],
                date      = doc["Date"],
                more_info = doc["More Info"],
                status    = doc["Status"],
                abstract  = doc["Abstract"],
                keywords  = doc["Keywords"],
                content   = doc["Content"]
            )

        writer.commit()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        MyWhoosh._prepare_folders_and_files()
        MyWhoosh._write_indexes()

    # #################################################################################################### #

    @staticmethod
    def _results_to_json(results):
        """Converte i risultati di Whoosh in un formato JSON-friendly."""
        
        results_list = []
        
        for result in results:
            
            result = dict(result)

            results_list.append(result)
        
        return json.dumps(results_list)  

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyWhoosh.INDEX_DIRECTORY_PATH):
            MyWhoosh.create_indexes()
        
        ### Esecuzione della query ###
        
        # Apertura dell'indice
        ix = index.open_dir(MyWhoosh.INDEX_DIRECTORY_PATH)

        # Corpo della query principale
        query = data["ricerca_principale"]

        # Logica dei Termini di Ricerca
        for t in data["terms"]:
            
            # Recupero dei valori del termine
            term = t["term"]
            op = t["operator"]
            field = t["field"].lower()

            # Traduzione dell'operatore NOT in AND NOT
            if op == "NOT":
                op = "AND NOT"

            # Costruzione della query (append)
            query = f'{query} {op} {field}:"{term}"'

        # Parserizza la Query
        query = QueryParser("content", ix.schema).parse(query)
        
        # Estrazione dei risultati
        with ix.searcher() as searcher:
            
            # Ottenimento dei rislutati
            results = searcher.search(query, limit=data.get("size"))
            
            # Formattazione dei Risultati
            results = MyWhoosh._results_to_json(results)
            
        return results
    
    # #################################################################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyWhoosh._execute_query(query)

# #################################################################################################### #

if __name__ == "__main__":
    MyWhoosh._prepare_folders_and_files()