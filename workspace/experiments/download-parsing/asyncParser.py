import asyncio
from typing import Optional, List, Dict
import json
import re
from aiohttp import ClientSession, ClientError
from bs4 import BeautifulSoup
from myLogger import logger as logging


class AsyncParser:

    # %%%%%% CLASS VARS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    TOTAL_RFC_NUMBER = 9688  # Numero totale di documenti disponibili
    DEFAULT_OUTPUT_FILE: str = "corpus.json"
    URL_METADATA: str = "https://www.rfc-editor.org/search/rfc_search_detail.php?page=All&pubstatus[]=Any&pub_date_type=any&abstract=abson&keywords=keyson&sortkey=Number&sorting=ASC"
    URL_PREFIX: str = "https://www.rfc-editor.org/rfc/rfc"
    URL_POSTFIX: str = ".html"

    # %%%%%% PAGES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    async def _download_page(session: ClientSession, url: str, timeout: int = 10) -> Optional[str]:
        """
        Scarica una singola pagina da un URL specificato in modo asincrono.
        """
        try:
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                return await response.text()
        except ClientError as e:
            logging.warning(f"Errore durante il download della pagina: {e}")
            return None

    @staticmethod
    async def _parse_page(html_content: str) -> Optional[Dict]:
        """
        Effettua il parsing del contenuto HTML in un dizionario.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # TODO: Rimozione header del documento. (Tramite regex?)
            text = soup.get_text().strip().replace('\n', ' ')
            text = re.sub(r'(\. \.)(?=\s)', '', text)
            text = re.sub(r' +', ' ', text)
            return text
        except Exception as e:
            logging.warning(f"Errore durante il parsing del contenuto HTML: {e}")
            return None

    @staticmethod
    async def _task(session: ClientSession, meta: dict) -> Optional[Dict]:
        """
        Scarica e parsifica una pagina specificata in modo asincrono.
        """
        url = AsyncParser.URL_PREFIX + meta['Number'] + AsyncParser.URL_POSTFIX
        html_content = await AsyncParser._download_page(session, url)
        if html_content is None:
            return None

        meta["Content"] = await AsyncParser._parse_page(html_content)
        return meta

    @staticmethod
    async def _download_and_parse_pages(metadata: List[dict], workers: int = 10) -> List[Dict]:
        """
        Scarica e parsifica più pagine in parallelo in modo asincrono.
        """
        async with ClientSession() as session:
            tasks = [AsyncParser._task(session, meta) for meta in metadata]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [res for res in results if res is not None]

    # %%%%%% METADATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    async def _download_and_parse_metadata(index_begin: int, index_end: int) -> Optional[List[dict]]:
        """
        Scarica e analizza i metadati di tutti gli RFC specificati in modo asincrono.
        """
        async with ClientSession() as session:
            try:
                async with session.get(AsyncParser.URL_METADATA) as response:
                    response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    table = soup.find("table", {"class": "gridtable"})
                    if not table:
                        logging.error("Tabella dei metadati non trovata.")
                        return None

                    rows = table.find_all("tr")[(index_begin * 3) - 2:(index_end * 3)]
                    return AsyncParser._parse_rows(rows)
            except ClientError as e:
                logging.error(f"Errore durante il download dei metadati: {e}")
                return None

    @staticmethod
    def _parse_rows(rows: list[any]) -> Optional[List[dict]]:
        """
        Analizza un insieme di righe HTML e ne estrae i metadati.
        """
        parsed_data = []

        for i in range(0, len(rows), 3):
            group = rows[i:i + 3]
            parsed = AsyncParser._parse_group(group)
            if parsed:
                parsed_data.append(parsed)

        return parsed_data

    @staticmethod
    def _parse_group(group: list[any]) -> Optional[dict]:
        """
        Analizza un gruppo di righe (metadati, abstract, keywords).
        """
        try:
            element = group[0].find_all("td")
            current = {
                "Number": element[0].get_text().split('\u00a0')[1].split(' ')[0].strip(),
                "Files": [tf.strip() for tf in element[1].get_text().replace('\u00a0', ' ').split(',')],
                "Title": element[2].get_text().replace('\u00a0', ' ').strip(),
                "Authors": [au.strip() for au in element[3].get_text().replace('\u00a0', ' ').split(',')],
                "Date": element[4].get_text().replace('\u00a0', ' ').strip(),
                "More Info": element[5].get_text().replace('\u00a0', ' ').strip(),
                "Status": element[6].get_text().replace('\u00a0', ' ').strip(),
                "Abstract": AsyncParser._parse_optional_row(group, 1, False),
                "Keywords": AsyncParser._parse_optional_row(group, 2, True)
            }
            return current
        except (IndexError, AttributeError) as e:
            logging.warning(f"Errore durante il parsing del gruppo: {e}")
            return None

    @staticmethod
    def _parse_optional_row(group, index: int, to_list: bool) -> list[str] | str:
        """
        Analizza una riga opzionale (Abstract o Keywords).
        """
        if len(group) > index:
            row = group[index].find_all("td")
            if len(row) > 1:
                if to_list:
                    return [item.strip() for item in row[1].get_text().split(',') if len(item) > 1]
                else:
                    return row[1].get_text().strip()
        return ""

    # %%%%%% GENERATE CORPUS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    async def generate_corpus(
        index_begin: int = 1, index_end: int = None, output_file: str = None, workers: int = 10
    ) -> None:
        """
        Genera un corpus scaricando e parsificando le pagine specificate in modo asincrono.
        """
        index_end = index_end if index_end is not None else AsyncParser.TOTAL_RFC_NUMBER
        output_file = output_file if output_file is not None else AsyncParser.DEFAULT_OUTPUT_FILE

        metadata = await AsyncParser._download_and_parse_metadata(index_begin, index_end)
        if metadata is None:
            logging.error("Impossibile generare il corpus. Nessun metadato disponibile.")
            return

        pages = await AsyncParser._download_and_parse_pages(metadata, workers)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=4)
        logging.info(f"Corpus salvato in {output_file}.")


# UNIT TESTING
if __name__ == "__main__":
    import time

    start = time.time()
    asyncio.run(AsyncParser.generate_corpus(index_begin=1, index_end=100))
    end = time.time()

    tot = str(end - start).split(".")
    print("Tempo esecuzione:", tot[0] + "." + tot[1][:4], "secondi")
