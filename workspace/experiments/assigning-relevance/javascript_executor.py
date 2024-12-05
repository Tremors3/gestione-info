from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

from time import sleep

# TUTORIAL PLAYWRIGHT (Con button click): https://blog.apify.com/python-playwright/

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
ua2 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"

with sync_playwright() as p:
    # Avvia il browser
    browser = p.chromium.launch(headless=True)
    context = browser.new_context() # user_agent=ua2
    page = context.new_page()
    
    #context = browser.new_context(
    #    viewport={"width": 1920, "height": 1080},
    #    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    #    geolocation={"latitude": 48.858844, "longitude": 2.294351},  # Esempio: Parigi
    #    permissions=["geolocation"]
    #)

    # Applica le tecniche stealth
    stealth_sync(page)
    
    # Naviga all'URL desiderato
    #url = "https://www.google.com/search?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F&num=100"
    #url = "https://duckduckgo.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F&num=100"
    url = "https://www.qwant.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Frfc-editor.org"
    page.goto(url)
    
    print("TEST3")
    # Attende che la pagina si carichi
    page.wait_for_load_state('networkidle')
    #page.wait_for_selector("a")
    print("TEST4")
    
    # TODO: Cliccare sul pulsante estendi risultati in base ai risultati necessari.

    # Estrai i link
    links = page.locator("a").all()
    
    # TESTING
    print(len(links))
    for link in links:
        if link: print(link.get_attribute("href"))

    #print(page.content())

    # Vars
    url_prefix = 'https://www.rfc-editor.org/rfc/rfc'
    documents = {}

    count = 1
    for link in links:
        attribute = link.get_attribute("href")
        if attribute is not None and url_prefix in attribute:
            rfc_number = attribute.removeprefix(url_prefix).split('.')[0]
            if rfc_number not in documents:
                documents[rfc_number] = {'document_id': rfc_number, 'position': count}
                count+=1

    from pprint import pprint
    pprint(documents)

    # Chiudi il browser
    
    context.close()
    browser.close()