import pg8000, os, json, sys
from typing import Optional
from time import sleep

from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

#from project.utils.metaclasses import Singleton
#from project.searchengine.myLogger.myLogger import bcolors, logging

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MyPostgres(metaclass=Singleton):
     
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    
    # #################################################################################################### #
    
    def __init__(self, 
            db_user:str="postgres", 
            db_password:str="postgres", 
            db_name:str="graboid_rfc", 
            address:str="127.0.0.1",
            port:int=55432,
            reconnect_attempts:int = 5,
            reconnect_interval:int = 0.5):
        """Inizializza la connessione al database con i parametri di configurazione."""
        
        self.db_password = db_password
        self.db_user = db_user
        self.db_name = db_name
        self.address = address
        self.port = port

        self.reconnect_attempts = reconnect_attempts
        self.reconnect_interval = reconnect_interval
        
        self.conn: Optional[pg8000.Connection] = None
        self._connect()
    
    # #################################################################################################### #
    
    def _connect(self):
        """Cerca di instaurare una connessione al database."""
        
        attempt = 0
        
        while attempt < self.reconnect_attempts:
        
            try:
        
                self.conn = pg8000.connect(
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.address,
                    port=self.port
                )
                print(f"Connessione al database \'{self.db_name}\' stabilita.")
                return
        
            except Exception as e:
                print(f"Connessione al database \'{self.db_name}\' non riuscita. Tentativo {attempt + 1}/{self.reconnect_attempts}.")
                sleep(self.reconnect_interval)
                attempt += 1
        
        raise ConnectionError("Impossibile connettersi al database.")

    def _reconnect(self):
        """Sovrascrive la connessione esistente con una nuova connessione."""
        print("Riconnessione al database...")
        self._connect()
    
    def _close_connection(self):
        """Chiude la connessione al database."""
        if self.conn:
            self.conn.close()
            print("Connessione al database chiusa.")
        else:
            print("Nessuna connessione attiva da chiudere.")
    
    def _get_cursor(self) -> Optional[pg8000.Cursor]:
        """Restituisce un cursore legato alla connessione."""
        if self.conn:
            return self.conn.cursor()
        print("Connessione non disponibile.")
        return None
    
    def __del__(self):
        """La connessione viene chiusa quando l'oggetto viene distrutto."""
        self._close_connection()
    
    # #################################################################################################### #
    
    def _initialize_table(self):
        """Crea la tabella per il dataset sovrascrivendo quella esistente"""
        cursor = self._get_cursor()
        
        try:
            
            cursor.execute('DROP TABLE IF EXISTS dataset;')
            cursor.execute("""
                CREATE TABLE dataset (
                    id integer PRIMARY KEY,
                    files text[],
                    title text,
                    authors text[],
                    date date,
                    more_info text,
                    status text,
                    abstract text,
                    keywords text[],
                    content text
                );
            """)
            self.conn.commit()
            print(f"Tabella creata con successo.")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Errore durante la creazione della tabella: {e}")
            raise
    
    @staticmethod
    def __sanitize(s: str) -> str:
        """Sanitizza le stringhe per evitare problemi con PostgreSQL."""
        s = s.replace('\\','\\\\')
        s = s.replace("'","\\'")
        s = s.replace('"','\\"')
        return s
    
    @staticmethod
    def __array_to_string(arr) -> str:
        """Converte una lista compatibile col tipo ARRAY di PostgreSQL."""
        #return "ARRAY[" + ",".join(f"E'{__class__.__sanitize(x)}'" for x in arr) + "]"
        return "ARRAY[E'" + "',E'".join(map(lambda x: __class__.__sanitize(x), arr)) + "']"
    
    @staticmethod
    def __get_documents():
        """Funzione che restituisce il contenuto del dataset."""
        if not os.path.isfile(__class__.DATASET_FILE_PATH):
            raise FileNotFoundError(f"Il file del dataset non è stato trovato al seguente percorso: \'{__class__.DATASET_FILE_PATH}\'.")
        
        with open(__class__.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            return json.load(f)

    def _populate_table(self, block_size: int = 500):
        """Popola la tabella con il dataset."""
        cursor = self._get_cursor()
        documents = __class__.__get_documents()
        
        insert_query = """
            INSERT INTO dataset (id, files, title, authors, date, more_info, status, abstract, keywords, content)
            VALUES {values};
        """

        try:
            
            with alive_bar(len(documents), title="Popolamento del database di PostgreSQL", spinner="waves", bar=_bar) as bar:
                
                insert_values = []
                
                for idx, doc in enumerate(documents, start=1):
                    
                    bar() # Progressing the bar
                    
                    id_ = doc["Number"]
                    files = __class__.__array_to_string(doc["Files"])
                    title = __class__.__sanitize(doc["Title"])
                    authors = __class__.__array_to_string(doc["Authors"])
                    date = doc["Date"]
                    more_info = __class__.__sanitize(doc["More Info"])
                    status = doc["Status"]
                    abstract = __class__.__sanitize(doc["Abstract"])
                    keywords = __class__.__array_to_string(doc["Keywords"])
                    content = __class__.__sanitize(doc["Content"])

                    insert_values.append("('{}', {}, E'{}', {}, to_date('{}', 'YYYY-MM'), E'{}', '{}', E'{}',  {}, E'{}')".format(
                        id_, files, title, authors, date, more_info, status, abstract, keywords, content
                    ))
                    
                    if (idx % block_size == 0) or (idx >= len(documents)): # default block size is 500
                        
                        cursor.execute(insert_query.format(
                            values=', '.join(insert_values)
                        ))
                        
                        self.conn.commit()
                        insert_values = []
                
                print("Popolamento del database completato.")
                
        except Exception as e:
            self.conn.rollback()
            print(f"Errore durante il popolamento del database: {e}")
            raise
    
    def _construct_indexes(self):
        """Crea gli indici sui campi specificati."""
        cursor = self._get_cursor()
        
        indexes = [
            "CREATE INDEX abstract_idx ON dataset USING GIN (to_tsvector('english', abstract));",
            "CREATE INDEX content_idx ON dataset USING GIN (to_tsvector('english', content));",
            "CREATE INDEX title_idx ON dataset USING GIN (to_tsvector('english', title));"
        ]
        
        try:
            
            for index in indexes:
                cursor.execute(index)
                print(f"Indice creato: {index}")
            
            self.conn.commit()
            print(f"Tutti gli indici sono stati creati correttamente.")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Errore durante la creazione degli indici: {e}")
            raise
    
    # #################################################################################################### #
    
    def create_indexes(self):
        """Pipeline di creazione degli indici."""
        self._initialize_table()
        self._populate_table()
        self._construct_indexes()
    
    def process(self, query: str = ""):
        cursor = self._get_cursor()
        
        results = cursor.execute(
            "SELECT id, ts_rank_cd(to_tsvector(content), query) AS rank FROM dataset, to_tsquery('QUIC & Protocol') query WHERE query @@ to_tsvector(content) ORDER BY rank DESC LIMIT 10;"
        )
        
        return results.fetchall()

    # #################################################################################################### #

def test_indexes_creation(postgres):
    postgres.create_indexes()

def test_query_execution(postgres):
    results = postgres.process({
        "ricerca_principale":"QUIC Protocol",
        "spelling_correction":False,
        "synonims":False,
        "search_engine":"PYLUCENE",
        "standard_track":True,
        "best_current_practice":False,
        "informational":False,
        "experimental":False,
        "historic":False,
        "standard_track_value":"PROPOSED_STANDARD",
        "date_year":"2021",
        "date_from_date":"2021-04",
        "date_to_date":"2021-06",
        "dates":"DATE_RANGE",
        "terms":[
            {
                "operator":"AND",
                "term":"QUIC",
                "field":"TITLE"
            },
            {
                "operator":"AND",
                "term":"document",
                "field":"DESCRIPTION"
            },
            {
                "operator":"NOT",
                "term":"network",
                "field":"KEYWORDS"
            }
        ],
        "abstracts":"True",
        "size":25
    })
    
    for doc in results: print(doc, '\n')

if __name__ == "__main__":
    postgres = MyPostgres()
    test_indexes_creation(postgres)
    test_query_execution(postgres)
    pass