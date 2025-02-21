
# Importazione standard
import pg8000, os, json, sys
from typing import Optional
from time import sleep

# # Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazione di moduli del progetto
from graboidrfc.core.modules.utils.metaclasses import Singleton
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# ################################################## #

class MyPostgres(metaclass=Singleton):
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    
    # INDEX & DATASET DIRECTORY PATHS
    DATASET_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "dataset", "dataset.json")
    
    # SETTINGS FILE PATHS
    SETTINGS_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "config", "postgres.json")
    
    # ################################################## #

    def __init__(self, use_docker: bool = False):
        """Inizializza la connessione al database."""
        
        # Lettura delle impostazioni
        settings = __class__.__get_settings()
        
        # Mapping impostazioni a parametri d'istanza
        self.__remap_settings(settings, use_docker)
        
        # Connecting to the database
        self.conn: Optional[pg8000.Connection] = None
        self._connect()
    
    # #################################################################################################### #
    
    def __remap_settings(self, settings, use_docker_port):
        """Funzione che mappa le impostazioni a variabili d'istanza."""
        try:
        
            # Network Settings
            self.port = settings["NETWORK_SETTINGS"]["PORT_NUMBER"] if not use_docker_port else settings["NETWORK_SETTINGS"]["DOCKER_PORT_NUMBER"]
            self.address = settings["NETWORK_SETTINGS"]["IP_ADDRESS"]
            
            # Reconnection Settings
            self.reconnect_attempts = settings["NETWORK_SETTINGS"]["RECONNECT_ATTEMPTS"]
            self.reconnect_interval = settings["NETWORK_SETTINGS"]["RECONNECT_INTERVAL"]
            
            # Database Settings
            self.db_password = settings["DATABASE_SETTINGS"]["DB_PASSWORD"]
            self.db_user = settings["DATABASE_SETTINGS"]["DB_USER"]
            self.db_name = settings["DATABASE_SETTINGS"]["DB_NAME"]

        except Exception as e:
            raise ValueError(f"Impossibile leggere il file di impostazione \'{__class__.SETTINGS_FILE_PATH}\': {e}")
    
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
    
    # #################################################################################################### #
    
    def _connect(self):
        """Cerca di instaurare una connessione al database."""
        
        attempt = 0 # Indice del tentativo
        
        while attempt < self.reconnect_attempts:
        
            try:
                
                # Tentativo di connessione
                self.conn = pg8000.connect(
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.address,
                    port=self.port
                )
                logging.info(f"Connessione al database \'{self.db_name}\' su \'{self.address}:{self.port}\' riuscita con successo.")
                return
        
            except Exception:
                logging.warning(f"Connessione al database \'{self.db_name}\' su \'{self.address}:{self.port}\' non riuscita. Tentativo {attempt + 1}/{self.reconnect_attempts}.")
                sleep(self.reconnect_interval)
                attempt += 1
        
        raise ConnectionError(f"Impossibile connettersi al database \'{self.db_name}\' su \'{self.address}:{self.port}\'. Controllare che il servizio di PostgreSQL sia attivo.")

    def _reconnect(self):
        """Sovrascrive la connessione esistente con una nuova connessione."""
        logging.info("Riconnessione al database...")
        self._connect()
    
    def _close_connection(self):
        """Chiude la connessione al database."""
        if self.conn:
            self.conn.close()
            logging.info("Connessione al database chiusa.")
        else:
            logging.info("Nessuna connessione attiva da chiudere.")
    
    def _get_cursor(self) -> Optional[pg8000.Cursor]:
        """Restituisce un cursore legato alla connessione."""
        if self.conn:
            return self.conn.cursor()
        logging.info("Connessione non disponibile.")
        return None
    
    def __del__(self):
        """La connessione viene chiusa quando l'oggetto viene distrutto."""
        pass #self._close_connection()
    
    # #################################################################################################### #
    
    def _initialize_table(self):
        """Crea la tabella per il dataset sovrascrivendo quella esistente"""
        
        # Ottenimento del cursore
        cursor = self._get_cursor()
        
        try:
            
            # Drop della tabella se esiste
            cursor.execute('DROP TABLE IF EXISTS dataset;')
            
            # La tabella viene ricreata
            cursor.execute("""
                CREATE TABLE dataset (
                    id          integer PRIMARY KEY,
                    files       text[],
                    title       text,
                    authors     text[],
                    date        date,
                    more_info   text,
                    status      text,
                    abstract    text,
                    keywords    text[],
                    
                    title_tsv    tsvector,
                    abstract_tsv tsvector,
                    keywords_tsv tsvector,
                    content_tsv  tsvector
                );
            """)
            
            # Commit
            self.conn.commit()

        except Exception as e:
            self.conn.rollback() # Rollback
            raise Exception(f"Errore durante la creazione della tabella: {e}")
    
    @staticmethod
    def __sanitize(s: str) -> str:
        """Sanitizza le stringhe per evitare problemi con PostgreSQL."""
        s = s.replace('\\','\\\\')
        s = s.replace("'","\\'")
        s = s.replace('"','\\"')
        return s
    
    @staticmethod
    def __array_to_string(arr) -> str:
        """Converte una lista python in ARRAY di PostgreSQL."""
        return "ARRAY[E'" + "',E'".join(map(lambda x: __class__.__sanitize(x), arr)) + "']"
    
    @staticmethod
    def __get_documents():
        """Funzione che restituisce il contenuto del dataset."""
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(__class__.DATASET_FILE_PATH):
            raise FileNotFoundError(f"Il file del dataset non è stato trovato al seguente percorso: \'{__class__.DATASET_FILE_PATH}\'.")
        
        # Apertura e lettura del dataset da file JSON e restituzione
        with open(__class__.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            return json.load(f)

    def _populate_table(self, block_size: int = 1000): # 1 <= bs <= 1000
        """Funzione che popola la tabella con il dataset."""
        
        # Ottenimento del cursore
        cursor = self._get_cursor()
        
        # Otteniemento dei documenti
        documents = __class__.__get_documents()
        
        # Template della query di inserimento
        insert_query = """
            INSERT INTO dataset (
                id,
                files,
                title,
                authors,
                date,
                more_info,
                status,
                abstract,
                keywords,
                
                title_tsv,
                abstract_tsv,
                keywords_tsv,
                content_tsv
            ) VALUES {values};
        """

        try:
            
            # Definizione della barra di caricamento che viene visualizzata durante l'esecuzione
            with alive_bar(len(documents), title="Popolamento del database di PostgreSQL", spinner="waves", bar=_bar) as bar:
                
                insert_values = [] # Ultimi "block_size" elementi
                
                # Ogni documento viene memorizzato nel database
                for idx, doc in enumerate(documents, start=1):
                    
                    bar() # Avanza la barra
                    
                    # Campi memorizzati
                    id_ = doc["Number"]
                    files = __class__.__array_to_string(doc["Files"])
                    title = __class__.__sanitize(doc["Title"])
                    authors = __class__.__array_to_string(doc["Authors"])
                    date = doc["Date"]
                    more_info = __class__.__sanitize(doc["More Info"])
                    status = doc["Status"]
                    abstract = __class__.__sanitize(doc["Abstract"])
                    keywords = __class__.__array_to_string(doc["Keywords"])
                    
                    # Campi indicizzati
                    title_tsv = title
                    abstract_tsv = abstract
                    content_tsv = __class__.__sanitize(doc["Content"])
                    keywords_tsv = __class__.__sanitize(' '.join(keywords))
                    
                    insert_values.append("""('{id}', {files}, E'{title}', {authors}, to_date('{date}', 'YYYY-MM'), E'{more_info}', '{status}', E'{abstract}', {keywords}, to_tsvector('english', E'{title_tsv}'), to_tsvector('english', E'{abstract_tsv}'), to_tsvector('english', E'{keywords_tsv}'), to_tsvector('english', E'{content_tsv}'))""".format(
                        
                        # Campi memorizzati
                        id=id_,
                        files=files,
                        title=title,
                        authors=authors,
                        date=date,
                        more_info=more_info,
                        status=status,
                        abstract=abstract,
                        keywords=keywords,
                        
                        # Campi indicizzati (TSector)
                        title_tsv=title_tsv,
                        abstract_tsv=abstract_tsv,
                        keywords_tsv=keywords_tsv,
                        content_tsv=content_tsv
                    ))
                    
                    # Operazione INSERT eseguita ogni block_size elementi (per motivi di efficienza).
                    if (idx % block_size == 0) or (idx >= len(documents)): # Default block size 1000
                        
                        # Esecuzione dell'inserizione
                        cursor.execute(insert_query.format(
                            values=', '.join(insert_values)
                        ))
                        
                        self.conn.commit() # Commit
                        insert_values = [] # Pulizia elementi inseriti

        except Exception as e:
            self.conn.rollback() # Rollback
            raise Exception(f"Errore durante il popolamento del database: {e}")
    
    def _construct_indexes(self):
        """Crea gli indici sui campi specificati."""
        
        # Ottenimento del cursore
        cursor = self._get_cursor()
        
        # Lista degli indici
        indexes = [
            "CREATE INDEX title_idx ON dataset USING GIN (title_tsv);",
            "CREATE INDEX abstract_idx ON dataset USING GIN (abstract_tsv);",
            "CREATE INDEX password_idx ON dataset USING GIN (keywords_tsv);",
            "CREATE INDEX content_idx ON dataset USING GIN (content_tsv);",
        ]
        
        try:
            
            # Creazione di ciascun indice
            for index in indexes:
                cursor.execute(index)
            
            self.conn.commit() # Commit

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Errore durante la creazione degli indici: {e}")
    
    # #################################################################################################### #
    
    def create_indexes(self):
        """Pipeline di creazione degli indici."""
        logging.debug("PostgreSQL: Inizializzazione della tabella e popolamento del database...")
        self._initialize_table()
        self._populate_table()
        logging.debug("PostgreSQL: Creazione degli indici sui campi...")
        self._construct_indexes()
    
    @staticmethod
    def _build_query(data: dict):
        """Costruzione della query da presentare a PostgreSQL."""
        
        definitions, conditions, statuses, ranks = [], [], [], []
    
        ############################################################
        ## QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO ##
        ############################################################
        
        # Otteniamo il valore della ricerca principale
        ricerca_principale = data.get("ricerca_principale")
        
        # Crea la definizione, il rank, e la condizione per la query principale
        definitions.append(f"LATERAL plainto_tsquery('english', '{ricerca_principale}') AS main")
        ranks.append(f"ts_rank_cd(content_tsv, main)")
        conditions.append(f"main @@ content_tsv")
        
        #######################################################################
        ## RICERCA SU PIU' CAMPI - CREAZIONE DI UNA QUERY BOOLEANA COMBINATA ##
        #######################################################################
        
        # Per ciascun termine secondario
        for idx, term in enumerate(data["terms"], start=1):
            
            # Recupero operatore e campo
            operator = term["operator"]
            term_value = term["term"]
            field = term["field"]

            # Crea la definizione
            definitions.append(f"LATERAL plainto_tsquery('english', '{term_value}') AS term{idx}")
            
            # Mappatura nome del campo
            field_mapping = {
                "TITLE": "title",
                "DESCRIPTION": "abstract",
                "KEYWORDS": "keywords"
            }; field = field_mapping[field]
            
            # Aggiungi il calcolo del ranking
            ranks.append(f"ts_rank_cd({field}_tsv, term{idx})")

            # Aggiungi la condizione appropriata
            if operator in ("AND", "NOT"):
                conditions.append(f"{operator} term{idx} @@ {field}_tsv".removeprefix("AND "))

        # Unisci tutte le condizioni, i ranking 
        # calcolati e le definizioni dei remini
        where_clause = " AND ".join(conditions)
        from_clause = ", ".join(definitions)
        rank_clause = " + ".join(ranks)
        
        ###########################################################################
        ## RICERCA PER STATO - CREAZIONE DI UNA QUERY PER LO STATO DEI DOCUMENTI ##
        ###########################################################################

        ## Pattern Matching documentation in Postgres
        # https://www.postgresql.org/docs/current/functions-matching.html

        # Verifica se i parametri per la ricerca dello stato sono abilitati
        run_status_search = any(data[key] for key in [
            "standard_track", "best_current_practice", "informational", "experimental", "historic"
        ])

        # Se ci sono parametri di stato
        if run_status_search:

            # Mappatura tra i parametri di stato e i valori di stato
            status_mapping = {
                "best_current_practice": "Best Current Practice",
                "informational": "Informational",
                "experimental": "Experimental",
                "historic": "Historic",
            }

            # Aggiungi lo stato specifico per "standard_track"
            if data["standard_track"]:
                
                # Estrai il valore specificato per "standard_track"
                value = data["standard_track_value"].strip().upper()
                
                # Mappatura dei valori dello "standard_track"
                standard_track_mapping = {
                    "PROPOSED_STANDARD": "Proposed Standard",
                    "DRAFT_STANDARD": "Draft Standard",
                    "INTERNET_STANDARD": "Internet Standard",
                }
                
                # Se il valore specificato esiste nella mappatura
                if value in standard_track_mapping:
                    # Aggiungi la query per lo stato
                    standard_track = standard_track_mapping[value].lower()
                    statuses.append(f"status ILIKE \'%{standard_track}%\'")

            # Aggiungi gli altri stati mappati
            # ("Best Current Practice", "Informational", "Experimental", "Historic")
            for key, status in status_mapping.items():
                # Verifica che lo stato sia stato selezionato
                if data[key]:
                    # Aggiungi la query per lo stato
                    statuses.append(f"status ILIKE \'%{status}%\'")
        
        statuses_clause = " AND ({statuses})".format(statuses=" OR ".join(statuses)) if statuses else ""
        
        ############################################################################
        ## RICERCA PER DATA - CREAZIONE DI UNA QUERY PER IL FILTRAGGIO SULLE DATE ##
        ############################################################################
        
        ## Date filtering documentation for Postgres
        # https://www.postgresql.org/docs/current/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE
        # https://www.postgresql.org/docs/current/functions-formatting.html

        date_query = "" # Valore di default per la date query
        date_filter = data.get("dates", "").strip().upper() # Opzione selezionata

        # Se l'opzione selezionata è "ALL_DATES", non filtriamo per data
        if date_filter != "ALL_DATES":
            
            # Filtro per anno specifico (SPECIFIC_YEAR)
            if date_filter == "SPECIFIC_YEAR" and (data["date_year"]):
                
                specific_year_int = data.get("date_year")

                if specific_year_int:
                    # Crea la query per l'anno specifico
                    date_query = f"EXTRACT(YEAR FROM date) IS NOT DISTINCT FROM {specific_year_int}"

            # Filtro per intervallo tra date (DATE_RANGE)
            elif date_filter == "DATE_RANGE" and (data["date_from_date"] and data["date_to_date"]):
                
                from_date_str = data.get("date_from_date")
                to_date_str = data.get("date_to_date")

                if from_date_str and to_date_str:
                    # Crea la query per l'intervallo di date
                    date_query = f"date BETWEEN to_date('{from_date_str}', 'YYYY-MM') AND to_date('{to_date_str}', 'YYYY-MM')"
    
        date_clause = f" AND ({date_query})" if date_query else ""
        
        ###########################################################################
        ## COSTRUZIONE DELLA QUERY FINALE - COMBINAZIONE DELLE QUERY INDIVIDUALI ##
        ###########################################################################
        
        # Stringa contenente i campi da ritirare
        select_clause = "id AS number, abstract, authors, to_char(date, 'YYYY-MM') AS date, files, keywords, more_info, status, title"
        
        # Crea la query che sarà presentata a postgres
        base_query = "SELECT json_agg(d) documents FROM ( SELECT {select_clause}, {rank_clause} AS rank FROM dataset, {from_clause} WHERE {where_clause}{statuses_clause}{date_clause} ORDER BY rank DESC LIMIT {size} ) d;"
        final_query = base_query.format(select_clause=select_clause, rank_clause=rank_clause, from_clause=from_clause, where_clause=where_clause, statuses_clause=statuses_clause, date_clause=date_clause, size=data["size"])
        
        # Restituzione
        return final_query

    def process(self, data: dict):
        
        # Ottenimento del cursore
        cursor = self._get_cursor()
        
        # Creazione eformattazione della query
        final_query = __class__._build_query(data)
        
        # Esecuzione della query e ottenimento dei risultati
        results = cursor.execute(final_query).fetchall()

        # Restituzione risultati
        return results[0][0]

    # #################################################################################################### #

if __name__ == "__main__":

    """
    SELECT id AS number, abstract, authors, date, files, keywords, more_info, status, title,
        ts_rank_cd(content_tsv, main) + ts_rank_cd(title_tsv, term1) + ts_rank_cd(abstract_tsv, term2) + ts_rank_cd(keywords_tsv, term3) AS rank
    FROM dataset,
        LATERAL plainto_tsquery('english', 'QUIC Protocol') AS main,
        LATERAL plainto_tsquery('english', 'QUIC') AS term1,
        LATERAL plainto_tsquery('english', 'document') AS term2,
        LATERAL plainto_tsquery('english', 'network') AS term3
    WHERE main @@ content_tsv
        AND term1 @@ title_tsv
        AND term2 @@ abstract_tsv
        AND NOT term3 @@ keywords_tsv
        AND (status ILIKE '%proposed standard%'
            OR status ILIKE '%Best Current Practice%'
            OR status ILIKE '%Informational%'
            OR status ILIKE '%Experimental%'
            OR status ILIKE '%Historic%')
        AND (EXTRACT(YEAR FROM date) IS NOT DISTINCT FROM 2021)
    ORDER BY rank DESC
    LIMIT 25
    """
    
    data = {
        "ricerca_principale":"QUIC Protocol",
        "spelling_correction":False,
        "synonims":False,
        "search_engine":"POSTGRES",
        "standard_track":True,
        "best_current_practice":False,
        "informational":False,
        "experimental":False,
        "historic":False,
        "standard_track_value":"PROPOSED_STANDARD", # PROPOSED_STANDARD | DRAFT_STANDARD | INTERNET_STANDARD
        "date_year":"2021",
        "date_from_date":"2021-04",
        "date_to_date":"2021-06",
        "dates":"DATE_RANGE", # SPECIFIC_YEAR | DATE_RANGE
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
    }
    
    def test_indexes_creation(postgres):
        postgres.create_indexes()

    def test_query_execution(postgres, data):
        results = postgres.process(data)
        for doc in results: print('\n', doc)
    
    def test_query_construction(data):
        print('\n', MyPostgres._build_query(data))
    
    postgres = MyPostgres()
    #test_indexes_creation(postgres)
    #test_query_execution(postgres, data)
    test_query_construction(data)