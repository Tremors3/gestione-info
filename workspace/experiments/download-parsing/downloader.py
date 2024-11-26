import time
import requests
import concurrent.futures
from typing import Optional, Generator

class Downloader:
    
    TOTAL_RFC_NUMBER = 9688
    
    @staticmethod
    def _download_page(session: requests.Session, url: str, timeout: int = 10) -> Optional[str]:
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text  # Restituisce il contenuto HTML della pagina
        except requests.exceptions.RequestException as e:
            print(f"\aErrore durante il download della pagina: {e}")
            return None  # Restituisce None se si verifica un errore

    @staticmethod
    def _download_section_parallel(
        url_prefix: str, url_postfix: str, 
        index_begin: int, index_end: int,
        workers: int
    ) -> Generator[str, None, None]:
        with requests.Session() as session:  # Usa la sessione per ottimizzare le richieste
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                
                # Crea lista di tutti gli URL dei siti da scaricare
                urls = [f"{url_prefix}{index}.{url_postfix}" for index in range(index_begin, index_end + 1)]
                
                # SUBMITTARE I JOBS - "JOBS SUBMITTING"
                futures = {
                    executor.submit(
                        Downloader._download_page,  # Ogni job dovrà scaricare una pagina
                        session,                   # utilizzando la stessa sessione html
                        url                        # con il relativo url
                    ): url for url in urls
                }

                # Per ogni task, quando è finita, restituisci il contenuto HTML della pagina
                for future in concurrent.futures.as_completed(futures):
                    page = future.result()
                    if page is not None:
                        yield page  # Restituisce il contenuto HTML della pagina

    @staticmethod
    def download_page(url_prefix: str, url_postfix: str = "html") -> Optional[str]:
        # Metodo per scaricare una singola pagina
        url = f"{url_prefix}.{url_postfix}"
        with requests.Session() as session:
            return Downloader._download_page(session, url)

    @staticmethod
    def download_section(
        url_prefix: str, 
        url_postfix: str = "html", 
        index_begin: int = 1, 
        index_end: Optional[int] = None, 
        workers: int = 10
    ) -> Generator[str, None, None]:
        
        if index_end is None:
            index_end = Downloader.TOTAL_RFC_NUMBER
        
        # Restituisce il generatore che scarica la sezione di documenti in parallelo
        yield from Downloader._download_section_parallel(url_prefix, url_postfix, index_begin, index_end, workers)

# UNIT TESTING
if __name__ == "__main__":
    start = time.time()
    for page in Downloader.download_section("https://www.rfc-editor.org/rfc/rfc"): pass
    end = time.time()
    print("Tempo esecuzione: ", end - start, " secondi")




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
                    

# Ci sono dei dati che se mancano scartiamo l'intera pagina, se invece sono dai meno importanti li rimpiazziamo con dei placeholder generici o valori nulli.

                    
                    