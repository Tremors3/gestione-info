import numpy as np
import pandas as pd

# Esempio di dati: ogni motore restituisce una lista di documenti con posizione
risultati_motori = [
    {"motore": "google", "documenti": [{"document_id": "rfc1234", "posizione": 1},
                                       {"document_id": "rfc2345", "posizione": 2},
                                       {"document_id": "rfc3456", "posizione": 5}]},
    {"motore": "duckduckgo", "documenti": [{"document_id": "rfc1234", "posizione": 2},
                                           {"document_id": "rfc2345", "posizione": 3},
                                           {"document_id": "rfc4567", "posizione": 10}]},
    {"motore": "bing", "documenti": [{"document_id": "rfc1234", "posizione": 1},
                                     {"document_id": "rfc4567", "posizione": 4},
                                     {"document_id": "rfc3456", "posizione": 7}]}
]

# Parametro di peso per il consenso (frequenza)
alpha = 0.5

# Funzione per calcolare il punteggio di rilevanza in base alla posizione
def calcola_rilevanza(posizione):
    return 1 / np.log2(posizione + 1)

# Aggregare i dati: sommare i punteggi di rilevanza per ogni documento
aggregati = {}

for motore in risultati_motori:
    for doc in motore["documenti"]:
        doc_id = doc["document_id"]
        posizione = doc["posizione"]
        rilevanza = calcola_rilevanza(posizione)
        
        if doc_id not in aggregati:
            aggregati[doc_id] = {"document_id": doc_id, "punteggio_totale": 0, "frequenza": 0}
        
        aggregati[doc_id]["punteggio_totale"] += rilevanza
        aggregati[doc_id]["frequenza"] += 1

# Convertire in lista e calcolare il punteggio finale
documenti = []
for doc_id, valori in aggregati.items():
    punteggio_finale = valori["punteggio_totale"] * (1 + alpha * valori["frequenza"])
    documenti.append({"document_id": doc_id, "punteggio_rilevanza": punteggio_finale})

# Normalizzare i punteggi in un range 0-3
punteggi = [doc["punteggio_rilevanza"] for doc in documenti]
min_punteggio, max_punteggio = min(punteggi), max(punteggi)

def normalizza_punteggio(punteggio, min_p, max_p):
    return 3 * (punteggio - min_p) / (max_p - min_p)

# Assegnare valori discreti di rilevanza (0, 1, 2, 3)
for doc in documenti:
    rilevanza_normalizzata = normalizza_punteggio(doc["punteggio_rilevanza"], min_punteggio, max_punteggio)
    doc["rilevanza_normalizzata"] = round(rilevanza_normalizzata)

# Creare un DataFrame per visualizzare i risultati
df = pd.DataFrame(documenti)

print(df)