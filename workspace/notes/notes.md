
# COSE DA FINIRE

### [da_finire] NOTA SULL'UTILIZZO DELLA SEARCH BAR

- [ ] Da completare.
   
   Nella sezione a destra dell'interfaccia grafica elenchiamo tre sezioni, una per Search Engine (Whoosh, Postgresql, Pylucene).
   All'interno di queste sezione specifichiamo le possibili grammatiche di funzionalità offerte dai vari search engine.

   A seconda del motore selezionato l'utente dovrà andare ad utilizzare la sintassi opportuna di quel motore.
   Le sintassi dei tre motori saranno mostrate di fianco al prompt della query, in modo che l'utente.

   In questo modo non dobbiamo ideare una sintassi comune e poi aggiustarla in base alla scelta del motore ma
   utilizziamo la sintassi diretta del motore così ci semplifichiamo la vita.

### [fatto] MODIFICARE ALCUNE COSE DEI TERMINI DI RICERCA

- [x] Rimuoviamo l'operatore OR perchè introduce molta logica difficile da gestire tra i diversi motori di Ricerca.

- [x] Rnominiamo "AND" ad "IN", mentre rinominiamo "NOT" ad "NOT IN"; in questo modo è più chiaro che non ci stiamo riferendo agli operatori AND e OR ma al fatto che all'interno dei campo i termini devono esserci o no in modo esatto. E' un podo per essere più chiari e precisi.
      - L'abbiamo semplicemente effettuato la rinomina da frontend sulla pagina web. I valori presentati sono `NOT` e `NOT IN`, mentre i valori effettivi sono `AND` e `NOT`.

# COSE DA FARE

### [fatto] MODERNIZZAZIONE DELLA STRUTTURA DEGLI SCRIPT DI AVVIO DEL SISTEMA

- [x] Modernizzare l'avvio del sistema. Mi riferisco agli script "graboid" e "starter".
      Per adesso i due script utilizzano sys per il recupero degli argomenti di sistema.
      Suggerisco l'utilizzo di strumenti più sofisticati e adatti allo scopo come "argparser" visto a lezione di Complementi.

      Inoltre voglio ridefinire i comandi e le opzioni possibili in modo da avere:
        - [x] - un comando che consente di inizializzare e nel caso reinizializzare il progetto da capo;
        - [x] - diversi comandi che consentono di eseguire singolarmente le varie sezioni della pipeline di inizializzazione;
        - [x] - altri comandi che consentono di avviare l'applicazione web e le altre funzionalità.

### [fatto] ORGANIZZARE LA CLASSE DI WHOOSH + RIFORMULARE DEMO WHOOSH

- [x] Riorganizzare la demo di whoosh facendo tutti i controlli necessari, mettendo apposto i percorsi, ecc...

### [fatto] QUANDO VENGONO CREATI GLI INVERTED INDEX dei SEARCH ENGINE ?

- [x] Gli indici di tutti i modelli di ranking e dei vari sistemi devono essere creati subito dopo il download dei documenti tramite il parser.
      Ogni volta che viene ricreato il dataset devono venir ricreati anche tutti gli indici dei vari sistemi e modelli.

      - [x] - Indici di Whoosh Funzionanti
      - [x] - Indici di pyLucene Funzionanti
      - [x] - Indici di Postgress Funzionanti

### [fatto] I TRE SEARCH ENGINE DEVONO POTER ESEGUIRE LE QUERY CON TUTTI I DIVERSI PARAMETRI AGGIUNTIVI

RICERCA PER DATA
- La ricerca per data per PyLucene è stata implementata in post-processing; cioè dopo la ricerca applicata da pylucene.

Whoosh
- [x] - Query Principale (Supportata)
- [x] - Ricerca per Termini (Supportata)
- [x] - Ricerca per Stato (Supportata)
- [x] - Ricerca per Data (Supportata)

PyLucene
- [x] - Query Principale (Supportata)
- [x] - Ricerca per Termini (Supportata)
- [x] - Ricerca per Stato (Supportata)
- [x] - Ricerca per Data (Supportata)

Postgress
- [x] - Query Principale (Supportata)
- [x] - Ricerca per Termini (Supportata)
- [x] - Ricerca per Stato (Supportata)
- [x] - Ricerca per Data (Supportata)

- [x] - Sistemare commenti.

### [fatto] CREARE LO SCRIPT SEPARATO PER GESTIONE DI PYLUCENE [OPPURE] RINUNCIARE AGLI SCRIPT DI AVVIO E PACCHETTIZZARE L'APP PER L'INSTALLAZIONE

- [NO] Bisogna creare uno script che consenta di utilizzare da linea di comando pylucene perchè non è possibile utilizzarlo nell'ambiente virtuale su cui va il webserver purtroppo. Si potrebbe cercare di installare pylucene all'interno del venv ma è praticamente impossibile e richiederebbe troppo tempo. Pylucene verrà gestito interamente da uno script specializzato realizzato "ad-hok", possibilmente utilizzando ArgumentParser.

#### OPPURE

- [SI] Invece di utilizzare uno script alternativo con l'unico scopo di permettere l'utilizzazione di PyLucene, possiamo invece pacchettizzare e permettere l'installazione del programma come mostratoci dal prof in Complementi di Programmazione. Sarà compito della prof gestire il venv in cui è installata l'applicazione. Questo non vuol dire che dovremo cancellare gli script "graboid.py" e "starter.py"; restano ottimi per il testare parti di programma.

- [x] Trovare il modo di installare l'applicazione:
    1. RIORGANIZZAZIONE GERARCHICA COMPLETA DEL PROGETTO:
        - [x] Riorganizza la gerachia in cartelle e correggi gli import
        - [x] Sposta il dataset e le configurazioni nelle relative nuove cartelle e correggi i percorsi
        - [x] Aggiornare il modo con cui tutti gli script costruiscono i percorsi (soprattutto gli script vecchi).
    2. Script simile a start che consente di utilizzare l'applicazione;
        - [x] Scrivi lo script e testa l'installazione.
        - [x] Correggi prefisso a tutti i percorsi.
        - [x] Correggi percorsi dinamici ai file.
        - [x] Avvia la macchina virtuale e far funzionare pylucene con il resto del sistema.
    3. Definisci la procedura di installazione del progetto e delle rispettive dipendenze.
        - [x] Descrivi prima tutta la procedura su un file md.
        - [x] Scrivi il file README.md del progetto con la procedura di installazione.
        - [x] Testa l'intera procedura di installazione su una nuova macchina virtuale Ubuntu. E aggiungi eventuali passi mancanti alla procedura di installazione.
            - [x] Test su WSL2/Ubuntu (Windows 11)
            - [x] Test su VirtualBox/Ubuntu
            - [x] Test su VirtualBox/Debian
        - [x] Correggi e completa il README (errore "i" mancante) e fai in modo che si segua in maniera più lineare.
        - [x] Correggi l'errore del link nel README: [Clona](#-installazione-pacchetto)

- [x] Rendere docker opzionale:
   - [x] Normalmente l'applicazione deve leggere potersi collegare al servizio PostgreSQL senza docker
   - [x] Opzionalmente tramite flags aggiuntive è possibile specificare di voler utilizzare docker

- [x] Utilizza il Logger e migliora le stampe di tutti i moduli. Poi prova ad inizializzare in modo da vedere se sono abbastanza belle.

- [x] Pare che alcune funzionalità di ricerca non eseguono correttamente su PyLucene (mentre eseguono correttamente sugli altri due motori)
    - [x] Clausola "NOT IN" in PyLucene non sembra funziona correttamente.
    - [x] Clausole "SPECIFIC YEAR" in Pylucene non sembra funzionare correttamente.

### [fatto] RISTRUTTURARE GLI SCRIPT DI CREAZIONE DEL BANCHMARK:
- [x] Invece di salvare l'intero link solamente il numero identificativo del documento;
- [x] Aggiungere e formattare commenti in modo che le stampe siano belle;
- [x] Risistemazione generale degli scripts.

### [da_fare] STABILIRE UNA FASE COMUNE DI PREPROCESSING ED IMPLEMENTARLA

UNICA PIPELINE DI PREPROCESSING vs UTILIZZARE QUELLE FORNITE DAI SE.
- [ ] Stabilire una fase di preprocessing comune per tutti i search engine e testare Stemmer, Lemmatizer, Parsers, Taggers, Rimozione Stopwords, ecc... Questa fase comune a tutti i search engine potrebbe essere implementata direttamente dal web server. Oppure utilizzando la pipeline di preprocessing fornita da ciascun search engine.

SPELLING CORRECTION & SYNONIMS
- [ ] E' meglio che togliamo la SPELLING CORRECTION e i SINONIMI (Espansione delle query con termini sinonimi)? Non mi sembra molto difficile da implementare e inoltre l'implementazione sarebbe comune a tutti e tre i search engine... per esempio utilizzando la libreria NLTK. Ma conviene farlo?
   - [ ] Scaricare i dizionari necessari durante la fase di inizializzazione.
   - [ ] Spelling Correction & Synonims (Non Ancora Supportata)

### [da_fare] RIVISITA DEL BENCHMARK E SELEZIONE DEI MODELLI DI RANKING E CONFRONTO TRA I MODELLI

- [x] Scegliere due modelli di ranking per ciascun motore di ricerca e altrettante varianti per ciascun modello.
    - [x] Whoosh     $\rightarrow$ ha **BM25** e **BM25 Custom**,       **TF_IDF**       e **TF_IDF_FF**.
    - [x] PyLuceme   $\rightarrow$ ha **BM25** e **BM25 Custom**,       **VSM (TF_IDF)** e **VSM (TFLN_PIDF)**.
    - [x] PostgreSQL $\rightarrow$ ha **BM25** e **BM25 Custom (DLN)**, **TF_IDF**       e **TF_IDF (DLN)**.

- [x] Fare in modo che sia possibile selezionare i Modelli di Ranking per ciascun sistema.
    - [x] L'interfaccia supporta la scelta della funzione di ranking.
    - [x] Per ciascun sistema utilizzare almeno tre modelli di ranking.
        - Whoosh
            - [x] Scelta dei modelli di ranking
            - [x] Implementazione modello personalizzato (Custom)
        - PyLucene
            - [x] Scelta dei modelli di ranking
            - [x] Implementazione modello personalizzato (Custom)
                Link alla classe da estendere: https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/similarities/SimilarityBase.html
            - [/] Trovare il modo di creare un indice per ciascun modello (--> Trovato come fare, ma non lo facciamo <--)
                Cosa cambia rispetto a impostare la Similarity solo nel Searcher?: https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/index/IndexWriterConfig.html#setSimilarity(org.apache.lucene.search.similarities.Similarity)
        - PostgreSQL
            - [x] Scelta dei modelli di ranking
            - [x] Implementazione modello personalizzato (Custom)

- [x] Rivisita del Benchmark. Migliorare l'ordinamento ideale dei documenti rispetto alle query (soprattutto quelle multi-valore).
    Gabri ha svolto un buon lavoro nel riordinare idealmente i risultati che compongono il benchmark.

- [x] Ottenere i ranking dei nostri tre sistemi di ricerca, formattarli in json come "extracted_local.json".
    Alla fine avremo "extracted_online.json" e "extracted_local.json" e poi il benchmark "benchmark.json" relativo ai risultati online.

- [ ] Confrontare le varianti dei nostri tre motori di ricerca:
    - [ ] Progettare e Realizzare lo script che definisce le formule e attua i confronti tra le varianti dei sistemi tenendo conto dei risultati del benchmark.
    - [ ] Ottenere i grafici che mostrano i confronti tra le varianti dei motori di ricerca.
        - [ ] Salvare i grafici in modo che siano visualizzabili.
    - [ ] Decidere le metriche da utilizzare per confrontare i sistemi:
        1. F-MESURE
        2. AVERAGE PRECISION (LEVEL)
        3. AVERAGE PRECISION (QUERY)
        4. MEAN AVERAGE PRECISION (MAP)
        5. DISCOUNTED CUMULATIVE GAIN (DCG & NDCG)
        6. PRECISION AT STANDARD RECALL LEVELS
    - [ ] Automatizzare il processo che effettua i controlli:
        1. creazione del benchmark, 
        2. scaricamento dei risultati delle query, 
        3. confronto dei risultati con formule e tecniche appropriate.

- [ ] Aggiustare i parametri `k1` e `b` dei ranking **BM25** sia di **WHOOSH** sia di **PYLUCENE** tramite sperimentazione.

- [ ] Una volta completata l'interfaccia grafica incorporare su github immagini che mostrino la stessa; e che siano visibili dal README.md.

# OBIETTIVI
### 1. FUNZIONI PER VALUTARE I MODELLI DI RANKING
### 2. REALIZZARE GRAFICI
### 3. COMPLETARE DOCUMENTAZIONE
### 4. REALIZZARE PRESENTAZIONE
