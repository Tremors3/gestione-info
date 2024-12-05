from urllib.parse import urlencode
from bs4 import BeautifulSoup
from time import sleep
import logging
import requests

# Configurazione del logger
logging.basicConfig(level=logging.INFO)

class Searcher:
    
    SITES = {
        "GOOGLE": {
            "base_url": "https://www.google.com/search",
            "query_param": "q",
            "specifier": "site:{site}",
        },
        "DUCKDUCKGO": {
            "base_url": "https://duckduckgo.com/",
            "query_param": "q",
            "specifier": "site:{site}",
        }
    }

    def __init__(self, query: str, target: str, engine: str):
        """
        Inizializza la classe Searcher.
        :param query: La query di ricerca.
        :param target: Il sito target (es. "www.rfc-editor.org/rfc").
        :param engine: Il motore di ricerca ("GOOGLE" o "DUCKDUCKGO").
        """
        self.query = query.strip()
        self.target = target.strip()
        self.engine = engine.strip().upper()
        
        if not self.query:
            raise ValueError("La query di ricerca non può essere vuota.")
        if not self.target:
            raise ValueError("Il sito target non può essere vuoto.")
        if self.engine not in Searcher.SITES:
            raise ValueError(f"Motore di ricerca '{self.engine}' non supportato.")

    def _build_url(self):
        """
        Costruisce l'URL per la ricerca in base al motore selezionato.
        """
        engine_config = Searcher.SITES[self.engine]
        query = f"{self.query} {engine_config['specifier'].format(site=self.target)}"
        params = {engine_config["query_param"]: query}
        url = f"{engine_config['base_url']}?{urlencode(params)}"
        logging.info(f"URL costruito per {self.engine}: {url}")
        return url

    def _download_page(self, url: str, session: requests.Session, timeout: int = 10, delay_ms: int = 5):
        """
        Scarica una singola pagina da un URL specificato.
        """
        try:
            sleep(delay_ms / 1000.0)  # Ritardo per evitare blocchi
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.warning(f"Errore durante il download della pagina: {e}")
            return None

    def _get_linked_urls(self, html: str):
        """
        Estrae i link dall'HTML.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        return links

    def execute_search(self):
        """
        Esegue la ricerca utilizzando il motore selezionato.
        """
        url = self._build_url()
        with requests.Session() as session:
            html = self._download_page(url, session)
            if not html:
                logging.warning("Nessun contenuto HTML recuperato.")
                return []

            results = self._get_linked_urls(html)
            logging.info(f"Risultati trovati ({len(results)}): {results}")
            return results


if __name__ == '__main__':
    TARGET = "www.rfc-editor.org/rfc"
    QUERY = "QUIC protocol"
    ENGINE = "GOOGLE"

    searcher = Searcher(query=QUERY, target=TARGET, engine=ENGINE)
    results = searcher.execute_search()
    from pprint import pprint
    pprint(results)
