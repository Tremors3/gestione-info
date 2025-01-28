import os, sys, json, shutil

# #################################################################################################### #

import pg8000 as pos

# #################################################################################################### #

from project.searchengine.myLogger.myLogger import logger as logging, bcolors

# #################################################################################################### #

class MyPostgres:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    # INDEX_DIRECTORY_PATH = os.path.join(CURRENT_FILE_PATH, "indexes_dir")
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    
    # #################################################################################################### #

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyPostgres.DATASET_FILE_PATH):
            logging.error(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyPostgres.DATASET_FILE_PATH}\'.")
            sys.exit(1)
        
        # Controllo se la cartella degli indici esiste
        # if os.path.exists(MyPostgres.INDEX_DIRECTORY_PATH):
        #     # Se esiste la elimino
        #     shutil.rmtree(MyPostgres.INDEX_DIRECTORY_PATH)
        
        # Creazione della cartella degli indici
        # if not os.path.exists(MyPostgres.INDEX_DIRECTORY_PATH):
        #     os.mkdir(MyPostgres.INDEX_DIRECTORY_PATH)

    @staticmethod
    def _write_indexes():
        """ Funzione che scrive gli indici per la ricerca. """
        
        # Apertura del file del dataset
        with open(MyPostgres.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
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
        
        writer = index.create_in(MyPostgres.INDEX_DIRECTORY_PATH, SCHEMA).writer()

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
        MyPostgres._prepare_folders_and_files()
        MyPostgres._write_indexes()

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
        # if not os.path.exists(MyPostgres.INDEX_DIRECTORY_PATH):
        #     MyPostgres.create_indexes()
        
        ### Esecuzione della query ###
        
        # Apertura dell'indice
        # ix = index.open_dir(MyPostgres.INDEX_DIRECTORY_PATH)

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

        # Parsa la Query
        query = QueryParser("content", ix.schema).parse(query)
        
        # Estrazione dei risultati
        with ix.searcher() as searcher:
            
            # Ottenimento dei rislutati
            results = searcher.search(query, limit=data.get("size"))
            
            # Formattazione dei Risultati
            results = MyPostgres._results_to_json(results)
            
        return results
    
    # #################################################################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPostgres._execute_query(query)

# #################################################################################################### #

if __name__ == "__main__":
    MyPostgres._prepare_folders_and_files()