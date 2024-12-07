import asyncio
import random
from playwright.async_api import async_playwright

# Elenco di User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
]

# Altri header casuali
ACCEPT_LANGUAGE_OPTIONS = [
    #"en-US,en;q=0.9",
    "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    #"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    #"de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
]

REFERER_OPTIONS = [
    #"https://www.google.com/",
    #"https://www.bing.com/",
    "https://www.duckduckgo.com/",
    #"https://www.yahoo.com/",
]

ACCEPT_OPTIONS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html,application/json,application/xml;q=0.9,*/*;q=0.8",
    "application/json,text/html;q=0.8",
]

def generate_random_headers():
    """
    Genera un dizionario di header HTTP randomizzati.
    """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(ACCEPT_LANGUAGE_OPTIONS),
        "Referer": random.choice(REFERER_OPTIONS),
        "Accept": random.choice(ACCEPT_OPTIONS),
    }

async def fetch_randomized_request():
    async with async_playwright() as p:
        # Genera header casuali
        headers = generate_random_headers()

        # Avvia il browser e imposta gli header
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(extra_http_headers=headers)
        page = await context.new_page()
        
        # Naviga a un URL di esempio
        await page.goto("https://duckduckgo.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F")
        
        # Debug: stampa gli header usati
        print("HTTP Headers utilizzati:")
        for key, value in headers.items():
            print(f"{key}: {value}")
        
        # Stampa il contenuto della pagina
        print(await page.content())
        
        # Chiudi il browser
        await context.close()
        await browser.close()

# Esegui la funzione principale
asyncio.run(fetch_randomized_request())
