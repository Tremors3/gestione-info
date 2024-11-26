import requests
import concurrent.futures
from typing import Generator, Optional
import time

class Downloader:
    
    TOTAL_RFC_NUMBER = 9688
    
    @staticmethod
    def _download_page(session: requests.Session, url: str, timeout: int = 10) -> Optional[str]:
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text  # Restituisce il contenuto HTML della pagina
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download della pagina: {e}")
            return None  # Restituisce None se si verifica un errore

    @staticmethod
    def _download_section_parallel(
        url_prefix: str, url_postfix: str, 
        index_begin: int, index_end: int,
        workers: int):
        
        with requests.Session() as session:  # Usa la sessione per ottimizzare le richieste
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                
                # Crea lista di tutti gli URL dei siti da scaricare
                urls = [f"{url_prefix}{index}.{url_postfix}" for index in range(index_begin, index_end + 1)]
                
                # SUBMITTARE I JOBS - "JOBS SUBMITTING"
                # Creazione delle tasks da fare eseguire alla threadpool
                # ogni task è in realtà il download di una pagina web
                futures = {
                    executor.submit(
                        Downloader.download_page,  # Ogni job dovrà scaricare una pagina
                        session,                   # utilizzando la stessa sessione html
                        url                        # con il relativo url
                    ): url for url in urls
                }

                # Per ogni task constrolliamo quando è finita;
                # Quando la task è finita possiamo restituire il contenuto HTML della pagina web
                for future in concurrent.futures.as_completed(futures):
                    
                    #url = futures[future]
                    
                    page = future.result()
                    if page is not None:
                        yield page  # Restituisce il contenuto HTML della pagina

    @staticmethod
    def download_page(url_prefix: str, url_postfix: str="html"):
        return Downloader._download_page(url_postfix, url_postfix)
    
    @staticmethod
    def download_section(url_prefix: str, url_postfix: str="html", index_begin: int=1, index_end: int=None, workers: int=10):
        
        if index_end is None:
            index_end = Downloader.TOTAL_RFC_NUMBER
        
        yield Downloader._download_section_parallel(url_prefix, url_postfix, index_begin, index_end, workers)

# UNIT TESTING
if __name__ == "__main__":

    start = time.time()

    for page in Downloader.download_section("https://www.rfc-editor.org/rfc/rfc"): pass
    
    #for page in Downloader.download_section("https://www.rfc-editor.org/rfc/rfc", 1, 1000): pass
    
    end = time.time()
    print("Tempo esecuzione: ", end - start, " secondi")
    # print("Pagine non trovate: ", counter)




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

                    
                    