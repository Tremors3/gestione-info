#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Esegui una ricerca su DuckDuckGo
from duckduckgo_search import DDGS
#results = DDGS().text("QUIC protocol site:rfc-editor.org", max_results=25)

# Eseguiamo una lista di URL di esempio
results = [
    "https://www.rfc-editor.org/rfc/rfc9000.html",
    "https://www.rfc-editor.org/rfc/rfc9000.pdf",
    "https://www.rfc-editor.org/rfc/rfc8999.html",
    "https://www.rfc-editor.org/rfc/rfc9312.html",
    "https://www.rfc-editor.org/rfc/rfc9312.pdf",
    "https://www.rfc-editor.org/info/rfc9000",
    "https://www.rfc-editor.org/rfc/rfc9308.html",
    "https://www.rfc-editor.org/rfc/rfc9114.html",
    "https://www.rfc-editor.org/rfc/rfc9308.pdf",
    "https://www.rfc-editor.org/info/rfc9312",
    "https://www.rfc-editor.org/rfc/rfc9001.html",
    "https://www.rfc-editor.org/rfc/rfc9250.html",
    "https://www.rfc-editor.org/v3test/draft-ietf-quic-transport-34-bad-pdf-line-break.pdf",
    "https://www.rfc-editor.org/rfc/rfc9114.pdf",
    "https://www.rfc-editor.org/rfc/rfc8999.pdf",
    "https://www.rfc-editor.org/rfc/rfc9297.html",
    "https://www.rfc-editor.org/rfc/rfc9443.pdf",
    "https://www.rfc-editor.org/rfc/rfc9369.xml",
    "https://www.rfc-editor.org/info/rfc9308",
    "https://www.rfc-editor.org/rfc/rfc9250.pdf",
    "https://www.rfc-editor.org/rfc/rfc9250",
    "https://www.rfc-editor.org/rfc/rfc9221.html",
    "https://www.rfc-editor.org/rfc/rfc9114",
    "https://www.rfc-editor.org/rfc/rfc9221.pdf"
]

def extract_rfc_number(url):
    """
    Estrae il numero RFC dall'URL, se presente.
    """
    if "rfc-editor.org/rfc/rfc" in url:
        # Rimuovi il prefisso 'https://www.rfc-editor.org/rfc/rfc' e prendi il numero
        rfc_part = url.removeprefix("https://www.rfc-editor.org/rfc/rfc").split('.')[0]
        return rfc_part
    return None

def get_rfc_params():
    """
    Estrae i numeri RFC dai risultati e tiene traccia solo della posizione migliore.
    """
    # Dizionario per tenere traccia della posizione migliore per ogni RFC
    best_positions = {}

    for pos, result in enumerate(results):
        
        # Estrai il numero RFC dall'URL
        rfc_number = extract_rfc_number(result)
        if rfc_number:
            
            # Se il numero RFC non è presente o la nuova posizione è migliore
            if rfc_number not in best_positions or pos < best_positions[rfc_number]["posizione"]:
                best_positions[rfc_number] = {"document_id": rfc_number, "posizione": pos}

    # Converti il dizionario in una lista ordinata per posizione
    filtered_rfc_numbers = sorted(best_positions.values(), key=lambda x: x["posizione"])

    return filtered_rfc_numbers

duck_engine = {
    "motore": "duckduckgo", "documenti": get_rfc_params()
}

# Stampa i risultati
from pprint import pprint
pprint(duck_engine)