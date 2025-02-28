
# Importazione
import os, json

# Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazioni dei moduli del progetto
from graboidrfc.core.modules.engines.myWhoosh.myWhoosh import MyWhoosh
from graboidrfc.core.modules.engines.myPostgres.myPostgres import MyPostgres
from graboidrfc.core.modules.engines.myPylucene.myPylucene import MyPyLucene

# Importazioni altri moduli del progetto
from graboidrfc.core.modules.utils.logger import logging
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# ############################################################################ #

class ExtractorLocal():
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    
    QUERIES_CONFIG_FILE = os.path.join(
        DYNAMIC_PACKAGE_PATH, 
        "core", "data", "benchmark", "queries_definitive.json"
    )
    
    JSON_PATH = os.path.join(
        DYNAMIC_PACKAGE_PATH,  
        "core", "data", "benchmark", "extracted_local.json"
    )

    # Dizionario per i modelli di ranking dei search engine
    SEARCH_ENGINES = {
        
        "whoosh": [
            # BM25
            "BM25",
            "BM25_CUSTOM",
            # TFIDF
            "TFIDF",
            "TFIDF_CUSTOM",
        ],
        
        "pylucene": [
            # BM25
            "BM25",
            "BM25_CUSTOM",
            # VSM
            "VSM",
            "VSM_CUSTOM"
        ],
        
        "postgresql": [
            # BM25
            "BM25",
            "BM25_CUSTOM",
            # TFIDF
            "TFIDF",
            "TFIDF_CUSTOM",
        ],
    }
    
    @classmethod
    def __load_queries(cls) -> list[str]:
        """Carica le query dal file"""
        try:
            with open(cls.QUERIES_CONFIG_FILE) as f:
                query_doc = json.load(f)
        except Exception as e:
            file_ = cls.QUERIES_CONFIG_FILE
            logging.error(f"Errore durante l'apertura del file {file_}: {e}")

        queries = []
        for query in query_doc:
            queries.append(query.get("query"))

        return queries

    @staticmethod
    def __get_fields(text, fields: list) -> dict:
        """
        Estrazione dei campi su cui fare la ricerca.

        Esempio: 
        "TCP protocol and congestion control title:TCP abstract:Congestion Control"
        
        diventa
        {'title': 'TCP', 'abstract': 'Congestion Control'}
        """
        result = {}

        for field in fields:
            if f"{field}:" in text:
                
                # Prendi la parte dopo "<field>:"
                part = text.split(f"{field}:")[1]
                
                # Tolgo il campo appena trovato
                next_fields = fields[:]
                next_fields.remove(field)

                # Controllo se ci sono altri campi nella parte dopo "<field>:"
                for next_field in next_fields:
                    
                    # Tolgo gli altri campi
                    if f"{next_field}:" in part:
                        part = part.split(f"{next_field}:")[0]
                        
                # Salva
                result[field] = part.strip()
        
        return result

    @staticmethod
    def __terms_builder(fields: dict) -> list[dict]:
        """Costruzione del dizionario dei termini"""
        terms = []
        for field, term in fields.items():
            terms.append({
                'operator': 'AND', 
                'term'    : term,
                'field'   : field.upper()
            })

        return terms

    @staticmethod
    def __get_query(query: str, fields: list) -> str:
        """Estrazione della query principale"""
        q = [query]
        for field in fields:
            q = q[0].split(field)

        return q[0]

    @staticmethod
    def __build_query(query: str, ranking: str) -> list[dict]:
        """Costruzione della query"""
        
        fields = ["title", "abstract", "keywords"]
        
        ricerca_principale = __class__.__get_query(query, fields)
        
        terms = __class__.__terms_builder(
            __class__.__get_fields(query, fields)
        )

        built_query = {
            "ricerca_principale"    : ricerca_principale,
            "spelling_correction"   : False,
            "synonims"              : False,
            "whoosh_ranking"        : f"{ranking}",
            "pylucene_ranking"      : f"{ranking}",
            "postgresql_ranking"    : f"{ranking}",
            "standard_track"        : False,
            "best_current_practice" : False,
            "informational"         : False,
            "experimental"          : False,
            "historic"              : False,
            "standard_track_value"  : "PROPOSED_STANDARD",
            "date_year"             : None,
            "date_from_date"        : None,
            "date_to_date"          : None,
            "dates"                 : "ALL_DATES",
            "terms"                 : terms,
            "abstracts"             : "True",
            "size"                  : 25
        }

        return built_query

    @staticmethod
    def __execute_query(query, search_engine, ranking):
        """Esecuzione della query e restituzione dei risultati"""
        numbers = []
        
        if search_engine == "whoosh":
            results = MyWhoosh.process(__class__.__build_query(query, ranking))

        if search_engine == "pylucene":
            results = MyPyLucene.process(__class__.__build_query(query, ranking))

        if search_engine == "postgresql":
            results = MyPostgres().process(__class__.__build_query(query, ranking))

        for result in results:
            numbers.append(result.get("number"))

        return numbers

    @staticmethod
    def __get_results():
        """Crea la struttura per i risultati e la restituisce"""

        queries = __class__.__load_queries()

        # Calcolo lunghezza della barra di caricamento
        x = (len(queries)*len(__class__.SEARCH_ENGINES["postgresql"])) + \
            (len(queries)*len(__class__.SEARCH_ENGINES["pylucene"])) + \
            (len(queries)*len(__class__.SEARCH_ENGINES["whoosh"]))
        
        results = {}

        # Barra di caricamento
        with alive_bar(x, title="Risultati", spinner="waves", bar=_bar) as bar:

            for query in queries:
                results[query] = {}

                for search_engine, functions in __class__.SEARCH_ENGINES.items():
                    results[query][search_engine] = {}
                    
                    for function in functions:

                        # Prendo tutti i risultati per una query eseguita con
                        # uno specifico search engine e funzione di ranking
                        results[query][search_engine][function] = __class__.__execute_query(
                            query, search_engine, function
                        )

                        # Avanzamento della barra
                        bar()
        
        return results

    @staticmethod
    def save_results_to_file(results: dict, filepath: str):
        """Salva i risultati in un file JSON."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise IOError(f"Errore nel salvataggio del file {filepath}: {e}")

    def start():
        
        # Apertura connessione PostgreSQL
        postgres = MyPostgres()
        
        results = ExtractorLocal.__get_results()
        
        # Chiusura connessione PostgreSQL
        postgres._close_connection()
        
        ExtractorLocal.save_results_to_file(
            results  = results, 
            filepath = __class__.JSON_PATH
        )