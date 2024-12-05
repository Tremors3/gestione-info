#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from duckduckgo_search import DDGS

    
# Esegui una ricerca su DuckDuckGo
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

def safe_int_cast(value, type_cast, default):
    try:
        return type_cast(value)
    except Exception as e:
        print(f"Errore durante la conversione di '{value}': {e}")
        return default

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






"""
Ciao. Sono uno studente univesritario del corso di Gestione Dell'informazione. La prof ci ha dato il compito di sviuluppare un search engine utilizzando whoosh. Come dataset abbiamo scelto di utilizzare l'insieme di documenti degli RFC (circa 9000). Adesso però per valutare le performance del nostro search necessitiamo di un benchmark. Il benchmark sono un piccolo sottoinsieme di documenti (rfc) con assegnato un valore di rilevanza per 10 query. Abbiamo i documenti rilevanti per ciascuna delle dieci query, ma non sappiamo come determinarne la rilevanza nei confronti della query. I documenti li abbiamo ottenuti cercando su altri search engine (google, duckduckgo, ecc...). Per determinare la rilevanza di un documento avevo in mente di:
1. Rilevanza più alta più il documento si trova tra i primi risultati.
2. Rilevanza più alta per i documenti tra i primi risultati che ci sono stati restituiti da più searchengine.
Hai dei consigli da darci per determinare meglio la rilevanza? Che formule possiamo utilizzare per determinare e normalizzare la rilevanza dei documenti? Es. 0=non rilevante, 1=rilevanza media, 2=rilevante, 3=molto rilevante. Come possiamo attribuire questi valori in modo sensato?
"""











