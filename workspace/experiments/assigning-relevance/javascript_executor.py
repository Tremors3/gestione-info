from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Avvia il browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Naviga all'URL desiderato
    #url = "https://www.google.com/search?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F&num=100"
    url = "https://duckduckgo.com/?q=QUIC+protocol+site%3Ahttps%3A%2F%2Fwww.rfc-editor.org%2Frfc%2F&num=100"
    page.goto(url)

    # Attendi che la pagina si carichi
    page.wait_for_load_state('networkidle')

    # Estrai i link
    links = page.locator("a").all()
    for link in links:
        print(link.get_attribute("href"))

    # Chiudi il browser
    browser.close()