import requests, logging, json, os

from dotenv import load_dotenv
from typing import Callable

def safecast(value, to_type, default=None):
    """Funzione per castare in modo sicuro"""
    try: return to_type(value)
    except (ValueError, TypeError):
        return default

# ################################################## #

class SearchEngine:
    """Classe per rappresentare un motore di ricerca e le sue impostazioni."""

    def __init__(self, name, base_url, default_params, extract=None):
        
        # Inizializzazione Parametri
        self.name = name
        self.base_url = base_url
        self.default_params = default_params
        
        # Inizializzazione Parametri Opzionali
        self.extract: Callable = extract or SearchEngine.base_extract
    
    @staticmethod
    def base_extract(url): return url
    
    def search(self, query, api_key):
        """Esegue una ricerca su questo motore di ricerca."""
        
        # Aggiornamento parametri richiesta
        params = self.default_params.copy()
        params.update({"api_key": api_key, "q": query})
        
        try:
            
            # Esecuzione della richiesta
            response = requests.get(self.base_url, params=params)

            # Verifica dello stato di risposta
            if response.status_code == 200:
                
                # Estrazione dei dati
                data = response.json()
                
                # Estrazione dei risultati di interesse
                organic_results = data.get("organic_results", [])

                # Estrazione dei numeri RFC dai risultati
                results = [rfc_number for result in organic_results if (rfc_number := self.extract(result.get("link"))) is not None]

                # Restituzione risultati
                return results

            else:
                
                # Errore durante la richiesta
                logging.error(f"Errore: {self.name} - {response.status_code} - {response.text}")
                return []
        
        # Errore durante il download della pagina
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore durante il download della pagina: {e}")
            return []

# ################################################## #

class RFCExtractor:
    """Classe principale per gestire i motori di ricerca e le query."""

    def __init__(self, api_key, config_file, 
                 supported_engines=None, 
                 serp_api_base_url=None, 
                 site_restrictor=None):
        
        # Inizializzazione Parametri
        self.api_key = api_key
        self.engines = []
        self.queries = []
        
        # Inizializzazione Parametri Opzionali
        self.supported_engines = supported_engines or {"google", "duckduckgo", "bing"}
        self.serp_api_base_url = serp_api_base_url or "https://serpapi.com/search"
        self.site_restrictor = site_restrictor or "site:www.rfc-editor.org"
        
        # Caricamento delle Configuraizoni
        self._load_config(config_file)

    def _load_config(self, config_file):
        """Carica la configurazione dei motori di ricerca e delle query dal file JSON."""
        try:
            
            # Caricamento delle Configurazioni
            with open(config_file, 'r') as file:
                config = json.load(file)    
                self._load_engines(config.get("engines", []))
                self._load_queries(config.get("queries", []))
                
        except FileNotFoundError:
            logging.error(f"File di configurazione '{config_file}' non trovato.")
        except json.JSONDecodeError:
            logging.error(f"Errore nel parsing del file JSON '{config_file}'.")

    def _load_engines(self, engines_config):
        """Carica i motori di ricerca dalla configurazione."""
        
        # Per ciascun motore di ricerca
        for engine in engines_config:
            name = engine.get("name")
            params = engine.get("params", {})
            base_url = self.serp_api_base_url
            
            # Verifica se il motore di ricerca è supportato
            if not name in self.supported_engines:
                logging.warning(f"Motore di ricerca '{name}' non supportato.")
                continue
            
            # Aggiunta specifica dell'engine
            params.update({"engine": name})
            
            # Aggiungi il motore di ricerca
            self.engines.append(SearchEngine(name, base_url, params, RFCExtractor.extract_rfc_number))

    def _load_queries(self, queries_config):
        """Carica le query dalla configurazione."""
        self.queries = ["{query} {site}".format(query=query.get("query"), site=self.site_restrictor) for query in queries_config]

    def execute_requests(self):
        """Esegue le richieste per tutte le query su tutti i motori di ricerca."""
        results = {}
        
        # Per ciascuna query
        for query in self.queries:
            
            results[query] = {} # Init Risultati per Query
        
            # Per ciascun motore di ricerca
            for engine in self.engines:
                logging.info(f"Eseguendo la query '{query}' su '{engine.name}'.")
                
                # Eseuzione della ricerca e salvataggio risultati
                links = engine.search(query, self.api_key)
                results[query][engine.name] = links
                
        return results

    @staticmethod
    def extract_rfc_number(url):
        """Estrae il numero RFC dall'URL, se presente."""
        
        prefixes = [
            "https://www.rfc-editor.org/rfc/rfc", 
            "https://www.rfc-editor.org/info/rfc"
        ]
        
        # FIltraggio degli URL
        for prefix in prefixes:
            if url.startswith(prefix):
                
                # Estrazione del numero dell'RFC
                return url.removeprefix(prefix).split('.')[0]
                #return safecast(rfc_num_str, int, None)
        
        return None

# ################################################## #

def write_results(file_name, results):
    """Scrive i risultati in un file JSON."""
    
    data = [
        {"query": query, "results": engines}
        for query, engines in results.items()
    ]

    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Errore durante la scrittura dei risultati: {e}")

def print_results(results):
    """Stampa i risultati in un formato leggibile."""
    print("Risultati:")
    for query, engines in results.items():
        print(f"\nQuery: {query}")
        for engine, links in engines.items():
            print(f"  Motore: {engine}")
            for link in links:
                print(f" - {link}", end=None)

# ################################################## #

def start():
    """Funzione principale per eseguire il programma."""
    
    load_dotenv(dotenv_path=".env")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise RuntimeError("Chiave API non trovata. Assicurati che sia configurata in '.env'.")

    config_file = "extractor.json"
    results_file = "extracted.json"

    # Inizializza l'estrattore
    extractor = RFCExtractor(api_key, config_file)

    # Esegue le richieste
    results = extractor.execute_requests()

    # Salva i risultati su file
    write_results(results_file, results)

    # Stampa i risultati
    print_results(results)

if __name__ == "__main__":
    start()