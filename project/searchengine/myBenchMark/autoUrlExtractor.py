from dotenv import load_dotenv
import requests
import logging
import json
import os

class SearchEngine:
    """Classe per rappresentare un motore di ricerca e le sue impostazioni."""

    def __init__(self, name, base_url, default_params):
        self.name = name
        self.base_url = base_url
        self.default_params = default_params

    def search(self, query, api_key):
        """Esegue una ricerca su questo motore di ricerca."""
        
        params = self.default_params.copy()
        
        params.update({
            "q": query,
            "api_key": api_key
        })
        
        try:
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                
                data = response.json()
                organic_results = data.get("organic_results", [])

                links = [result.get("link") for result in organic_results]
                return links
            
            else:
                
                logging.error(f"Errore: {response.status_code} - {response.text}")
                return []
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore durante il download della pagina: {e}")
            return None


class AutoUrlExtractor:
    """Classe principale per gestire i motori di ricerca e le query."""

    def __init__(self, api_key, config_file):
        self.api_key = api_key
        self.engines = []
        self.queries = []
        self._load_config(config_file)

    def _load_config(self, config_file):
        """Carica la configurazione dei motori di ricerca e delle query dal file JSON."""
        try:
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
        for engine in engines_config:
            name = engine.get("name")
            params = engine.get("params", {})
            base_url = self._get_engine_base_url(name)
            if base_url:
                self.engines.append(SearchEngine(name, base_url, params))
            else:
                logging.warning(f"Motore di ricerca '{name}' non supportato.")

    @staticmethod
    def _get_engine_base_url(engine_name):
        """Ritorna l'URL base per il motore di ricerca specificato."""
        base_urls = {
            "google": "https://serpapi.com/search",
            "duckduckgo": "https://serpapi.com/search",
            "bing": "https://serpapi.com/search"
        }
        return base_urls.get(engine_name)

    def _load_queries(self, queries_config):
        """Carica le query dalla configurazione."""
        self.queries = [query.get("query") for query in queries_config]

    def execute_requests(self):
        """Esegue le richieste per tutte le query su tutti i motori di ricerca."""
        results = {}
        for query in self.queries:
            results[query] = {}
            for engine in self.engines:
                logging.info(f"Eseguendo la query '{query}' su '{engine.name}'.")
                links = engine.search(query, self.api_key)
                results[query][engine.name] = links
        return results

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
                print(f"    - {link}")


def start():
    """Funzione principale per eseguire il programma."""
    load_dotenv(dotenv_path="secrets.env")
    api_key = os.getenv('API_KEY')

    if not api_key:
        raise RuntimeError("Chiave API non trovata. Assicurati che sia configurata in 'secrets.env'.")

    config_file = "queries.json"
    results_file = "results.json"

    # Inizializza l'estrattore
    extractor = AutoUrlExtractor(api_key, config_file)

    # Esegue le richieste
    results = extractor.execute_requests()

    # Salva i risultati su file
    write_results(results_file, results)

    # Stampa i risultati
    print_results(results)


if __name__ == "__main__":
    start()
