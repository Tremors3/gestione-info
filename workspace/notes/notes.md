
# SCELTA DEL DATASET
Abbiamo scelto di utilizzare come corpus i documenti RFC (Request for Comments) di Internet.  
## Perché abbiamo scelto questo corpus
### Molteplici Campi:
- Gli RFC sono suddivisi in sezioni standard (es. Introduzione, Motivazione, Specifiche, Conclusione), il che facilita la creazione di campi come titolo, autore, data, testo, e anche campi specifici come formule, tabelle, o header tecnici.
- Ogni RFC è numerato e ha un’identificazione univoca.
### Lunghezza e complessità variegate:
- Alcuni RFC sono brevi (es. RFC 1149, relativo alla trasmissione via piccioni), mentre altri sono molto lunghi e complessi (es. RFC 791, il protocollo IP).
### Applicabilità per query avanzate:
- Si possono formulare query che cercano informazioni in sezioni specifiche (es. "header TCP" nella sezione specifiche tecniche).
- I contenuti includono anche numeri, formule tecniche, tabelle, e diagrammi, utili per testare indicizzazioni e ottimizzazioni.














# INTRODUZIONE AL SEARCH ENGINE

## 1. A QUALE TIPOLOGIA DI UTENTI E' RIVOLTO IL SEARCH ENGINE?

## 2. QUALE TIPO QUERY LANGUAGE IMPLEMENTARE? (keyword based) (è un search engine).













# FASE 1: DOWNLOAD DEI DOCUMENTI

Downloader dei documenti.

# FASE 2: PARSING DEI DOCUMENTI

Gli RFC sono disponibili principalmente in formato testo puro o HTML, il che richiede un parser per estrarre i campi strutturati. Potresti dover fare parsing per separare i campi che saranno preprocessati nella fase successiva (es. titolo, abstract, e sezioni specifiche).

Sarà suddivisa in tre sezioni:
1. DOWNLOAD DEI DOCUMENTI
2. PARSING DEI CAMPI SCELTI
3. FORMATTAZIONE IN JSON
    - Thread Pool
      - Ogni thread: Utilizzatore del parser ().

DOBBIAMO AVERE IN MENTE
- I CAMPI

Ne decidiamo alcuni di base, poi li espanderemo in futuro in base ai bisogni.
Il parsing lo effettueremo con l'aiuto della libreria python pylucene.

# FASE 3: PREPROCESSING



# FASE 4: INDICIZZAZIONE








