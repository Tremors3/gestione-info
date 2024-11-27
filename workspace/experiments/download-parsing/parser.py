import json
import logging
import requests
import concurrent.futures
from typing import Optional, Generator, List, Dict
from bs4 import BeautifulSoup as soup

# Configurazione logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Parser:

    TOTAL_RFC_NUMBER = 9688  # Numero totale di documenti disponibili

    @staticmethod
    def _download_page(session: requests.Session, url: str, timeout: int = 10) -> Optional[str]:
        """Scarica una singola pagina da un URL specificato."""
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.warning(f"Errore durante il download della pagina: {e}")
            return None

    @staticmethod
    def _parse_page(html_content: str) -> Optional[Dict]:
        """Effettua il parsing del contenuto HTML in un dizionario."""
        # Sostituire con una logica di parsing reale
        try:

            #metas = soup.find_all('meta')
            #parsed_data['author'] = metas.find('')
            #for meta in soup.find_all('meta'):
            #    parsed_data[meta.get('name')] = meta['content']

            parsed_data = {}
            parsed_data = {"content": html_content[:200], "length": len(html_content)}  # Esempio

            return parsed_data
        except Exception as e:
            logging.warning(f"Errore durante il parsing del contenuto HTML: {e}")
            return None

    @staticmethod
    def _task(session: requests.Session, url: str) -> Optional[Dict]:
        """Scarica e parsifica una pagina specificata."""
        html_content = Parser._download_page(session, url)
        if html_content is None:
            return None
        return Parser._parse_page(html_content)

    @staticmethod
    def _download_and_parse(urls: List[str], workers: int = 10) -> Generator[Dict, None, None]:
        """Scarica e parsifica più pagine in parallelo."""
        with requests.Session() as session, concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

            futures = {
                executor.submit(Parser._task, session, url): url for url in urls
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    page = future.result()
                    if page is not None:
                        yield page
                except Exception as e:
                    logging.warning(f"Errore durante l'elaborazione di un task: {e}")

    @staticmethod
    def generate_corpus(
        url_prefix: str="https://www.rfc-editor.org/rfc/rfc", url_postfix: str="html",
        index_begin: int=1, index_end: int=TOTAL_RFC_NUMBER,
        output_file: str = "corpus.json",
        workers: int = 10
    ) -> None:
        """Genera un corpus scaricando e parsificando le pagine specificate."""

        # Creazione degli URL
        urls = [f"{url_prefix}{index}.{url_postfix}" for index in range(index_begin, index_end + 1)]

        # Scarica e parsifica le pagine
        page_list = []
        for page in Parser._download_and_parse(urls, workers):
            page_list.append(page)

        # Salva il corpus su file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(page_list, f, ensure_ascii=False, indent=4)
        logging.info(f"Corpus salvato in {output_file}.")

# UNIT TESTING
if __name__ == "__main__":
    import time
    start = time.time()
    Parser.generate_corpus(index_end=100)
    end = time.time()
    print("Tempo esecuzione: ", end - start, " secondi")







# https://www.ietf.org/rfc/

# Ci sono dei dati che se mancano scartiamo l'intera pagina, se invece sono dai meno importanti li rimpiazziamo con dei placeholder generici o valori nulli.

"""
dati da prendere dall'html

head
    meta: citation_author <-- IMPORTANTE, non in tutti gli rfc ci sono gli autori nel resto del documento
    meta: citation_publication_date
    meta: citation_title
    meta: citation_doi
    meta: citation_issn


body
    span: author
    bare: RESTO DELL'RFC


"""
