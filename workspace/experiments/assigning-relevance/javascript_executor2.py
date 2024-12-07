import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# User agents
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
ua2 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"

async def fetch_rfc_links():
    async with async_playwright() as p:
        # Avvia il browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        page = await context.new_page()
        
        # Applica le tecniche stealth
        await stealth_async(page)
        
        # Naviga all'URL desiderato
        #url = "https://www.google.com/search?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F&num=100"
        url = "https://duckduckgo.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F"
        #url = "https://www.qwant.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Frfc-editor.org"
        await page.goto(url)
        
        # Attende che la pagina si carichi
        await page.wait_for_load_state('networkidle')
        
        # Estrai i link
        links = await page.locator("a").all()
        
        await asyncio.sleep(5)
        
        # TESTING
        print(f"Numero di link trovati: {len(links)}")
        for link in links:
            href = await link.get_attribute("href")
            if href:
                print(href)
        
        print(await page.content())

        # Vars
        url_prefix = 'https://www.rfc-editor.org/rfc/rfc'
        documents = {}
        count = 1

        for link in links:
            attribute = await link.get_attribute("href")
            if attribute and url_prefix in attribute:
                rfc_number = attribute.removeprefix(url_prefix).split('.')[0]
                if rfc_number not in documents:
                    documents[rfc_number] = {'document_id': rfc_number, 'position': count}
                    count += 1

        # Stampa i risultati
        from pprint import pprint
        pprint(documents)

        # Chiudi il browser
        await context.close()
        await browser.close()

# Esegui la funzione principale
asyncio.run(fetch_rfc_links())
