
############################################################################################################

def get_duckduckgo_results(query: str, max_results: int = 25, auto: bool = False):
    
    if auto:
        
        # Esegui una ricerca su DuckDuckGo
        from duckduckgo_search import DDGS
        ddg = DDGS().text("QUIC protocol site:rfc-editor.org", max_results=max_results)
        results = [link for link in ddg if "rfc-editor.org" in link]
        print(results)
        return results
    
    return [
        'https://www.rfc-editor.org/rfc/rfc9000.html',
        'https://www.rfc-editor.org/rfc/rfc9000.pdf',
        'https://www.rfc-editor.org/rfc/rfc8999.html',
        'https://www.rfc-editor.org/info/rfc9000',
        'https://www.rfc-editor.org/rfc/rfc9312.html',
        'https://www.rfc-editor.org/rfc/rfc9308.html',
        'https://www.rfc-editor.org/rfc/rfc9114.html',
        'https://www.rfc-editor.org/rfc/rfc9312.pdf',
        'https://www.rfc-editor.org/rfc/rfc9001.html',
        'https://www.rfc-editor.org/rfc/rfc9308.pdf',
        'https://www.rfc-editor.org/rfc/rfc9250.html',
        'https://www.rfc-editor.org/rfc/rfc9114.pdf',
        'https://www.rfc-editor.org/rfc/rfc8999.pdf',
        'https://www.rfc-editor.org/rfc/rfc9297.html',
        'https://www.rfc-editor.org/rfc/rfc9443.pdf',
        'https://www.rfc-editor.org/rfc/rfc9369.xml',
        'https://www.rfc-editor.org/info/rfc9308',
        'https://www.rfc-editor.org/rfc/rfc9250.pdf',
        'https://www.rfc-editor.org/rfc/rfc9250',
        'https://www.rfc-editor.org/rfc/rfc9221.html',
        'https://www.rfc-editor.org/rfc/rfc9114',
        'https://www.rfc-editor.org/rfc/rfc9221.pdf',
        'https://www.rfc-editor.org/info/rfc9312',
        'https://www.rfc-editor.org/rfc/rfc9369.html',
        'https://www.rfc-editor.org/rfc/rfc9297.xml',
        'https://www.rfc-editor.org/rfc/rfc9001',
        'https://www.rfc-editor.org/rfc/rfc9443.html',
        'https://www.rfc-editor.org/rfc/rfc9001.xml',
        'https://www.rfc-editor.org/rfc/rfc9464.html',
        'https://www.rfc-editor.org/info/rfc8999',
        'https://www.rfc-editor.org/rfc/rfc9368.xml',
        'https://www.rfc-editor.org/rfc/rfc9001.pdf',
        'https://www.rfc-editor.org/rfc/rfc9298.html',
        'https://www.rfc-editor.org/rfc/rfc9308.xml',
        'https://www.rfc-editor.org/rfc/rfc9308',
        'https://www.rfc-editor.org/rfc/rfc9312.xml',
        'https://www.rfc-editor.org/rfc/rfc8999',
        'https://www.rfc-editor.org/rfc/rfc8446',
        'https://www.rfc-editor.org/rfc/rfc9297',
        'https://www.rfc-editor.org/rfc/rfc9000.xml',
        'https://www.rfc-editor.org/info/rfc9114',
        'https://www.rfc-editor.org/rfc/rfc9438.pdf',
        'https://www.rfc-editor.org/rfc/rfc4960',
        'https://www.rfc-editor.org/rfc/rfc7540.html',
        'https://www.rfc-editor.org/rfc/rfc9443.xml',
        'https://www.rfc-editor.org/rfc/rfc8323',
        'https://www.rfc-editor.org/rfc/rfc9330.html',
        'https://www.rfc-editor.org/rfc/rfc9002.xml',
        'https://www.rfc-editor.org/rfc/rfc9221',
        'https://www.rfc-editor.org/rfc/rfc9484.html',
        'https://www.rfc-editor.org/rfc/rfc9368.pdf',
        'https://www.rfc-editor.org/info/rfc9221',
        'https://www.rfc-editor.org/rfc/rfc9331.html',
        'https://www.rfc-editor.org/rfc/rfc9312',
        'https://www.rfc-editor.org/rfc/rfc9250.xml',
        'https://www.rfc-editor.org/info/rfc9002',
        'https://www.rfc-editor.org/rfc/rfc9221.xml',
        'https://www.rfc-editor.org/rfc/rfc9411.xml',
        'https://www.rfc-editor.org/rfc/rfc9147.html',
        'https://www.rfc-editor.org/rfc/rfc9002.html',
        'https://www.rfc-editor.org/rfc/rfc9114.xml',
        'https://www.rfc-editor.org/rfc/rfc9298',
        'https://www.rfc-editor.org/rfc/rfc9298.xml',
        'https://www.rfc-editor.org/rfc/rfc9170.html',
        'https://www.rfc-editor.org/rfc/rfc9204.html',
        'https://www.rfc-editor.org/rfc/rfc9369.pdf',
        'https://www.rfc-editor.org/rfc/rfc8546',
        'https://www.rfc-editor.org/rfc/rfc8899.html',
        'https://www.rfc-editor.org/rfc/rfc5730',
        'https://www.rfc-editor.org/info/rfc9297',
        'https://www.rfc-editor.org/rfc/rfc4960.html',
        'https://www.rfc-editor.org/rfc/rfc9368.html',
        'https://www.rfc-editor.org/rfc/rfc8744',
        'https://www.rfc-editor.org/rfc/rfc791',
        'https://www.rfc-editor.org/rfc/rfc6241',
        'https://www.rfc-editor.org/rfc/rfc9614.xml',
        'https://www.rfc-editor.org/rfc/rfc9220.html',
        'https://www.rfc-editor.org/rfc/rfc9260.html',
        'https://www.rfc-editor.org/rfc/rfc9204.xml',
        'https://www.rfc-editor.org/rfc/rfc9317.html',
        'https://www.rfc-editor.org/rfc/rfc9002',
        'https://www.rfc-editor.org/rfc/rfc9463.html',
        'https://www.rfc-editor.org/rfc/rfc9331.pdf',
        'https://www.rfc-editor.org/rfc/rfc9643.xml',
        'https://www.rfc-editor.org/rfc/rfc9113.pdf',
        'https://www.rfc-editor.org/rfc/rfc9420.html',
        'https://www.rfc-editor.org/rfc/rfc8922.xml',
        'https://www.rfc-editor.org/rfc/rfc9413.xml',
        'https://www.rfc-editor.org/rfc/rfc9113',
        'https://www.rfc-editor.org/rfc/rfc9298.pdf',
        'https://www.rfc-editor.org/rfc/rfc8484',
        'https://www.rfc-editor.org/rfc/rfc9287.xml'
    ][:max_results]

############################################################################################################

#from googlesearch import search

def get_google_results(query: str, max_results: int = 25, auto: bool = False):
    
    if auto:
        
        # Esegui una ricerca su DuckDuckGo
        from googlesearch import search
        
        # Esegui una ricerca su Google
        gr = search("QUIC protocol site:rfc-editor.org", num_results=max_results)
        results = [link for link in gr if "rfc-editor.org" in link]
        print(results)
        return results

    return [
        "https://www.rfc-editor.org/rfc/rfc9308",
        "https://www.rfc-editor.org/rfc/rfc9000.pdf",
        "https://www.rfc-editor.org/rfc/rfc9312.html",
        "https://www.rfc-editor.org/rfc/rfc8999.html",
        "https://www.rfc-editor.org/rfc/rfc9114.html",
        "https://www.rfc-editor.org/rfc/rfc9369.html",
        "https://www.rfc-editor.org/info/rfc9000",
        "https://www.rfc-editor.org/rfc/rfc9221.pdf",
        "https://www.rfc-editor.org/rfc/rfc9001",
        "https://www.rfc-editor.org/rfc/rfc9443.html",
        "https://www.rfc-editor.org/rfc/rfc9002",
        "https://www.rfc-editor.org/rfc/rfc9250.html",
        "https://www.rfc-editor.org/info/rfc9308",
        "https://www.rfc-editor.org/info/rfc9312",
        "https://www.rfc-editor.org/rfc/rfc9368.html",
        "https://www.rfc-editor.org/rfc/rfc9287.html",
        "https://www.rfc-editor.org/rfc/rfc8546.html",
        "https://www.rfc-editor.org/rfc/rfc8922.txt",
        "https://www.rfc-editor.org/info/rfc8999",
        "https://www.rfc-editor.org/rfc/rfc9297.html",
        "https://www.rfc-editor.org/rfc/rfc9298.html",
        "https://www.rfc-editor.org/rfc/rfc9317.html",
        "https://www.rfc-editor.org/rfc/rfc8802.html",
        "https://www.rfc-editor.org/rfc/rfc9265.xml",
        "https://www.rfc-editor.org/rfc/rfc8899",
        "https://www.rfc-editor.org/rfc/rfc9484.xml",
        "https://www.rfc-editor.org/rfc/rfc9065.txt",
        "https://www.rfc-editor.org/rfc/rfc9170.txt",
        "https://www.rfc-editor.org/rfc/rfc8470.html",
        "https://www.rfc-editor.org/info/rfc9369",
        "https://www.rfc-editor.org/rfc/rfc9506.txt",
        "https://www.rfc-editor.org/rfc/rfc9147.xml",
        "https://www.rfc-editor.org/rfc/rfc8774.xml",
        "https://www.rfc-editor.org/rfc/rfc9258.xml",
        "https://www.rfc-editor.org/rfc/rfc8558.html",
        "https://www.rfc-editor.org/rfc/rfc9292.xml",
        "https://www.rfc-editor.org/rfc/rfc9413.xml",
        "https://www.rfc-editor.org/rfc/rfc9325.txt",
        "https://www.rfc-editor.org/rfc/rfc8462.txt",
        "https://www.rfc-editor.org/rfc/rfc9419.txt",
        "https://www.rfc-editor.org/rfc/rfc9330.html",
        "https://www.rfc-editor.org/rfc/rfc9420.html",
        "https://www.rfc-editor.org/rfc/rfc9525",
        "https://www.rfc-editor.org/rfc/rfc9331.xml",
        "https://www.rfc-editor.org/info/rfc9443",
        "https://www.rfc-editor.org/rfc/rfc9439.xml",
        "https://www.rfc-editor.org/rfc/rfc9614.xml",
        "https://www.rfc-editor.org/rfc/rfc7934.txt",
        "https://www.rfc-editor.org/info/rfc9221",
        "https://www.rfc-editor.org/rfc/rfc9412.xml",
        "https://www.rfc-editor.org/info/rfc9114",
        "https://www.rfc-editor.org/rfc/rfc8323.html",
        "https://www.rfc-editor.org/rfc/rfc4960.html",
        "https://www.rfc-editor.org/errata/rfc9000",
        "https://www.rfc-editor.org/rfc/rfc9464.html",
        "https://www.rfc-editor.org/rfc/rfc9049.pdf",
        "https://www.rfc-editor.org/errata/rfc9312",
        "https://www.rfc-editor.org/rfc/rfc9473.xml",
        "https://www.rfc-editor.org/errata/eid7578",
        "https://www.rfc-editor.org/rfc/rfc9110.html",
        "https://www.rfc-editor.org/errata/eid7996",
        "https://www.rfc-editor.org/rfc/rfc9643.xml",
    ][:max_results]

############################################################################################################

def get_qwant_results(query: str, max_results: int = 25, auto: bool = False):
    
    if auto:
        pass
    
    return [
        "https://www.rfc-editor.org/rfc/rfc9308.html",
        "https://www.rfc-editor.org/rfc/rfc9000.pdf",
        "https://www.rfc-editor.org/rfc/rfc9312.html",
        "https://www.rfc-editor.org/rfc/rfc8999.html",
        "https://www.rfc-editor.org/rfc/rfc9114.pdf",
        "https://www.rfc-editor.org/info/rfc9369",
        "https://www.rfc-editor.org/rfc/rfc9221.html",
        "https://www.rfc-editor.org/rfc/rfc9001.html",
        "https://www.rfc-editor.org/rfc/rfc9443.pdf",
        "https://www.rfc-editor.org/info/rfc9002",
        "https://www.rfc-editor.org/rfc/rfc9250.html",
        "https://www.rfc-editor.org/rfc/rfc9368.html",
        "https://www.rfc-editor.org/rfc/rfc9287.pdf",
        "https://www.rfc-editor.org/rfc/rfc8546.pdf",
        "https://www.rfc-editor.org/rfc/rfc8922.html",
        "https://www.rfc-editor.org/rfc/rfc9297.pdf",
        "https://www.rfc-editor.org/rfc/rfc9298.xml",
        "https://www.rfc-editor.org/info/rfc9317"
    ][:max_results]

############################################################################################################
""" Otteniamo per ciascun RFC una correlazione tra CODICE_RFC e POSIZIONE dello stesso in un motore di ricerca. """

def extract_rfc_number(url):
    """Estrae il numero RFC dall'URL, se presente."""
    
    if "rfc-editor.org/rfc/rfc" in url:
        # Rimuovi il prefisso 
        # 'https://www.rfc-editor.org/rfc/rfc' e prendi il numero
        rfc_part = url.removeprefix("https://www.rfc-editor.org/rfc/rfc").split('.')[0]
        return rfc_part
    
    if "https://www.rfc-editor.org/info/rfc" in url:
        # Rimuovi il prefisso 
        # 'https://www.rfc-editor.org/info/rfc' e prendi il numero
        rfc_part = url.removeprefix("https://www.rfc-editor.org/info/rfc").split('.')[0]
        return rfc_part
    
    return None

def get_rfc_params(results: list):
    """Estrae i numeri RFC dai risultati e tiene traccia solo della posizione migliore."""
    
    # Dizionario per tenere traccia della posizione migliore per ogni RFC
    best_positions = {}

    position: int = 1
    for result in results:
        
        # Estrai il numero RFC dall'URL
        rfc_number = extract_rfc_number(result)
        if rfc_number:
            
            # Se il numero RFC non è presente o la nuova posizione è migliore
            if rfc_number not in best_positions:
                best_positions[rfc_number] = {"document_id": rfc_number, "posizione": position}
                position+=1

    # Converti il dizionario in una lista ordinata per posizione
    filtered_rfc_numbers = sorted(best_positions.values(), key=lambda x: x["posizione"])

    return filtered_rfc_numbers

############################################################################################################
""" Creazione una struttura dati che riorganizza i risultati per i vari motori di ricerca. """

MAX = 30

duck_results = get_duckduckgo_results("QUIC protocol site:rfc-editor.org", max_results=MAX, auto=False)
google_results = get_google_results("QUIC protocol site:rfc-editor.org", max_results=MAX, auto=False)
#qwant_results = get_qwant_results("QUIC protocol site:rfc-editor.org", max_results=25)

risultati_motori = [
    {"motore": "duckduckgo", "documenti": get_rfc_params(duck_results)},
    {"motore": "google", "documenti": get_rfc_params(google_results)}
    #{"motore": "qwant", "documenti": get_rfc_params(qwant_results)}
]

#from pprint import pprint
#pprint(risultati_motori)

############################################################################################################
""" Calcolo del fattore di rilevanza per ciascun documento. """
""" Nel calcolo viene considerata:
1. la POSIZIONE del termine rispetto ai risultati dei diversi motori di ricerca 
2. la FREQUENZA del termine rispetto ai motori di ricerca (in quanti motori di ricerca compare il termine) """

## ESEMPIO
#
# risultati_motori = [
#     {"motore": "google", "documenti": [{"document_id": "1234", "posizione": 1},
#                                        {"document_id": "2345", "posizione": 2},
#                                        {"document_id": "3456", "posizione": 5}]},
#     {"motore": "duckduckgo", "documenti": [{"document_id": "1234", "posizione": 2},
#                                            {"document_id": "2345", "posizione": 3},
#                                            {"document_id": "4567", "posizione": 10}]},
#     {"motore": "qwant", "documenti": [{"document_id": "1234", "posizione": 1},
#                                      {"document_id": "4567", "posizione": 4},
#                                      {"document_id": "3456", "posizione": 7}]}
# ]

import numpy as np

def calcola_rilevanza(posizione):
    return 1 / np.log2(posizione + 1)                                                              # FORMULA DI DECADUMENTO LOGARITMICO = SINGOLI PUNTEGGI DI RILEVANZA: R_t1, R_t2, ... R_tn

# Aggregare i dati: sommare i punteggi di rilevanza per ogni documento
aggregati = {}

for motore in risultati_motori:
    for doc in motore["documenti"]:
        
        doc_id = doc["document_id"]
        posizione = doc["posizione"]
        rilevanza = calcola_rilevanza(posizione)
        
        # Inizializzazione
        if doc_id not in aggregati:
            aggregati[doc_id] = {"document_id": doc_id, "punteggio_totale": 0, "frequenza": 0}
        
        # Sommatoria delle rilevanze
        aggregati[doc_id]["punteggio_totale"] += rilevanza                                         # SOMMA DEI DECADUMENTI LOGARITMICI = PUNTEGGIO DI RILEVANZA TOTALE: Rtot_t = R_t1 + R_t2 + ... + R_tn
        # Incremento della frequenza
        aggregati[doc_id]["frequenza"] += 1

# A questo punto i documenti hanno:
# 1. Rilevanza totale   (calcolata in base alle posizioni dello stesso documento ma nei tre motori di ricerca utilizzati)
# 2. Frequenza          (numero di search engine in cui il documento compare tra i risultati)

############################################################################################################
""" Questo frammento di codice calcola la rilevanza finale di ciascun documento, combinando: """
""" 1. Il punteggio di rilevanza basato sulla posizione nei risultati di ricerca. """
""" 2. La frequenza di apparizione nei vari motori di ricerca. """
""" La rilevanza finale viene poi normalizzata e arrotondata per ottenere un punteggio i nterpretabile. """

alpha = 1  # Peso della frequenza (0 <= alpha <= 1). Maggiore è alpha, più peso ha la frequenza.

documenti = []

# Calcolo della rilevanza finale combinando posizione e frequenza
for doc_id, valori in aggregati.items():
    # La formula combina il punteggio totale e la frequenza con un fattore di peso alpha
    punteggio_finale = valori["punteggio_totale"] * (1 + alpha * valori["frequenza"])              # FORMULA CHE UNISCE IL PUNTEGGIO DI RILEVANZA CON LA FREQUENZA
    # Salviamo il risultato in una lista di documenti
    documenti.append({"document_id": doc_id, "punteggio_rilevanza": punteggio_finale})

# Verifica che ci siano punteggi calcolati
if not documenti:
    raise ValueError("Non ci sono documenti per cui calcolare la rilevanza.")

# Normalizzazione dei punteggi in un range 0.0 - 2.0
punteggi = [doc["punteggio_rilevanza"] for doc in documenti]
min_punteggio, max_punteggio = min(punteggi), max(punteggi)

# Funzione per normalizzare i punteggi
def normalizza_punteggio(punteggio, min_p, max_p):
    if max_p == min_p:
        # Evitiamo divisioni per zero nel caso di punteggi identici
        return 2.0
    return 2 * (punteggio - min_p) / (max_p - min_p)                                               # NORMALIZZAZIONE DEL PUNTEGGIO

# Assegnazione dei punteggi normalizzati e arrotondati in un range 1-3
for doc in documenti:
    # Normalizzazione lineare dei punteggi
    rilevanza_normalizzata = normalizza_punteggio(doc["punteggio_rilevanza"], min_punteggio, max_punteggio)
    # Offset di 1 per mappare il range normalizzato (0.0-2.0) a (1.0-3.0)
    doc["rilevanza_normalizzata"] = rilevanza_normalizzata + 1
    # Arrotondamento per ottenere un valore discreto tra 1 e 3
    doc["rilevanza_normalizzata_arrotondata"] = round(rilevanza_normalizzata) + 1                  # POSIZIONAMENTO DEL PUNTEGGIO NEL RANGE DESIDERATO

############################################################################################################
""" Risultati Finali """

# Stampa dei risultati finali
print("Documenti con rilevanza calcolata:")
for doc in documenti:
    print(f"Rfc: {doc['document_id']},\t",
        f"Punteggio rilevanza: {doc['punteggio_rilevanza']:.5f},\t\t", 
        f"Rilevanza normalizzata: {doc['rilevanza_normalizzata']:.5f},\t", 
        f"Rilevanza normalizzata arrotondata: {doc['rilevanza_normalizzata_arrotondata']}"
    )

print("Totale documenti:", len(documenti), "su", MAX)

############################################################################################################
""" Miglioramenti Potenziali """

# Valutazione Umana:
#    Fai validare i risultati da revisori umani. Ad esempio, chiedi loro di classificare manualmente i documenti per almeno alcune query.
#
# Metriche di Benchmarking:
#    Valuta il tuo motore di ricerca rispetto al benchmark usando metriche standard come:
#        Precision@k: Percentuale di documenti rilevanti nei primi kk risultati.
#        Mean Average Precision (MAP): Media delle precisioni per tutte le query.
#        Normalized Discounted Cumulative Gain (NDCG): Valuta la qualità del ranking in relazione alla rilevanza.

############################################################################################################
""" Metriche standard per valutare le prestazioni """

# 1. Precision@k
#
#     Definizione: Percentuale di documenti rilevanti nei primi kk risultati.
#     Formula:
#     
#     $$ Precision@k = \frac{ \textit{\# documenti rilevanti nei primi k} } { \textit{k} } $$
#
#     Quando usarla:
#         - Per valutare rapidamente la qualità dei primi risultati.
#         - È particolarmente utile per motori di ricerca dove solo i primi risultati contano (come nel web search).
#
# Implementazione in Python:
def precision_at_k(relevanza_ottenuta, relevanza_attesa, k):
    """
    Calcola Precision@k.
    :param relevanza_ottenuta: Lista dei documenti restituiti ordinati (es. ['doc1', 'doc2', ...]).
    :param relevanza_attesa: Dizionario {document_id: rilevanza_attesa} (es. {'doc1': 3, 'doc2': 1}).
    :param k: Numero di risultati da considerare.
    :return: Precision@k (float).
    """
    risultati_k = relevanza_ottenuta[:k]
    rilevanti = sum(1 for doc in risultati_k if relevanza_attesa.get(doc, 0) > 0)
    return rilevanti / k
# Esempio di utilizzo
#relevanza_ottenuta = ["rfc9000", "rfc8999", "rfc9312"]
#relevanza_attesa = {"rfc9000": 3, "rfc9312": 2}  # 'rfc8999' non è rilevante
#k = 3
#print(f"Precision@{k}:", precision_at_k(relevanza_ottenuta, relevanza_attesa, k))






# 2. Mean Average Precision (MAP)
#
#     Definizione: Media delle precisioni calcolate a ogni documento rilevante.
#     Formula:
#
#     $$ AP = \frac{1}{R} \sum\limits_{k=1}^N Precision@k \cdot rilevanza(k) $$
#     $$ MAP = \frac{\sum_{q=1}^{Q}AP_q}{Q}
#
#     Dove:
#         $R$: Numero di documenti rilevanti.
#         $N$: Numero totale di documenti restituiti.
#         $Q$: Numero di query.
#
# Implementazione in Python:
def mean_average_precision(relevanza_ottenuta, relevanza_attesa):
    """
    Calcola Mean Average Precision (MAP).
    :param relevanza_ottenuta: Lista di documenti restituiti ordinati (es. ['doc1', 'doc2', ...]).
    :param relevanza_attesa: Dizionario {document_id: rilevanza_attesa} (es. {'doc1': 3, 'doc2': 1}).
    :return: MAP (float).
    """
    rilevanti = [doc for doc in relevanza_ottenuta if relevanza_attesa.get(doc, 0) > 0]
    if not rilevanti:
        return 0.0

    ap = 0.0
    rilevanti_trovati = 0
    for i, doc in enumerate(relevanza_ottenuta):
        if doc in rilevanti:
            rilevanti_trovati += 1
            ap += rilevanti_trovati / (i + 1)

    return ap / len(rilevanti)
# Esempio di utilizzo
#print("MAP:", mean_average_precision(relevanza_ottenuta, relevanza_attesa))






# 3. Normalized Discounted Cumulative Gain (NDCG)
#
#     Definizione: Valuta la qualità del ranking tenendo conto della posizione dei documenti rilevanti.
#     Formula:
#     
#     $$ DCG=\sum\limits_{i=1}^{N}\frac{2^{\textit{rilevanza}(i)}-1}{\log_2{i+1}} $$
#     $$ NDCG=\frac{DCG}{IDCG} $$
#     
#     Dove:
#         IDCGIDCG: DCG ideale, ottenuto da un ranking perfetto.
def ndcg(relevanza_ottenuta, relevanza_attesa, k):
    """
    Calcola NDCG@k.
    :param relevanza_ottenuta: Lista dei documenti restituiti ordinati.
    :param relevanza_attesa: Dizionario {document_id: rilevanza_attesa}.
    :param k: Numero di risultati da considerare.
    :return: NDCG@k (float).
    """
    def dcg(relevanze):
        return sum((2**rel - 1) / np.log2(idx + 2) for idx, rel in enumerate(relevanze))
    
    relevanze_ottenute = [relevanza_attesa.get(doc, 0) for doc in relevanza_ottenuta[:k]]
    dcg_val = dcg(relevanze_ottenute)
    
    relevanze_ideali = sorted(relevanza_attesa.values(), reverse=True)[:k]
    idcg_val = dcg(relevanze_ideali)
    
    return dcg_val / idcg_val if idcg_val > 0 else 0.0
# Esempio di utilizzo
#k = 3
#print(f"NDCG@{k}:", ndcg(relevanza_ottenuta, relevanza_attesa, k))






# Conclusione
#
# Puoi scegliere la metrica in base al tuo obiettivo:
#
#     Precision@k: Semplice e utile per valutare i primi risultati.
#     MAP: Ottimo per valutare la qualità complessiva dei risultati.
#     NDCG: Ideale per analizzare l'importanza delle posizioni e dei documenti rilevanti