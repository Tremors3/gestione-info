
# COSE DA FINIRE

### [da_finire(quello_di_postgresql)] NOTA SULL'UTILIZZO DELLA SEARCH BAR

Nella sezione a destra dell'interfaccia grafica elenchiamo tre sezioni, una per Search Engine (Whoosh, Postgresql, Pylucene).
All'interno di queste sezione specifichiamo le possibili grammatiche di funzionalità offerte dai vari search engine. Per esempio:

```
SEZIONE WHOOSH
Puoi effettuare una ricerca esatta tramite l'operatore ""<N>. i.e. "information retrieval"<3>

SEZIONE POSTGRESQL
Puoi effettuare una ricerca esatta tramite l'operatore ::-N- i.e. :information retrieval:-3-
```

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

### [da_fare] ORGANIZZARE LE CLASSI DI WHOOSH, PYLUCENE, E POSTGRESS + RIFORMULARE DEMO WHOOSH

- [ ] Riorganizzare la demo di whoosh facendo tutti i controlli necessari, mettendo apposto i percorsi, ecc...
- [ ] Realizzare il punto precedente in modo che lo schema organizzativo sia replicabile anche per pylucene e postgress.

### [da_fare] QUANDO VENGONO CREATI GLI INVERTED INDEX dei SEARCH ENGINE ?

- [ ] Gli indici di tutti i modelli di ranking e dei vari sistemi devono essere creati subito dopo il download dei documenti tramite il parser.
      Ogni volta che viene ricreato il dataset devono venir ricreati anche tutti gli indici dei vari sistemi e modelli.

      Per adesso funzione così (va automatizzato come scritto sopra):
            1. Cancellare la cartella "index_dir" di whoosh
            2. Rieseguire il parser
            3. Effettuare una ricerca (alla prima ricerca verrà effettuato l'indice)

### [da_fare] PROVARE I DIVERSI STEMMER / LEMMATIZER - IN GENERALE METTERE APPOSTO LA FASE DI PREPROCESSING

- [ ] Provare i diversi stemmer / lemmatizer; anche se rischiano di fare overstemming: per esempio cambiando "Quick" in "Quic" il protocollo, e ciò non va bene.

### [da_fare] FINIRE DI SCEGLIERE LE QUERY + OTTENERE BENCHMARK

- [ ] Scegliere le query e farle passare per lo script automatico che trova i documenti più rilevanti e ne restituisce la rilevanza.

POSSIBILI QUERY

```
### **Query 1**
1. **Query**: `content:"protocol"`  
2. **Linguaggio naturale**: *"Cerca tutti i documenti che contengono la parola 'protocol' nel contenuto."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe voler avere una panoramica generale sugli RFC relativi ai protocolli, senza un'idea specifica di quale cercare. È una ricerca esplorativa.  
4. **Motivo per cui la query è adatta per il test**:  
   Questa query è semplice e generica, utile per verificare che il search engine gestisca correttamente ricerche di termini comuni, con un'ampia gamma di risultati.

---

### **Query 2**
1. **Query**: `title:"Hypertext Transfer Protocol"`  
2. **Linguaggio naturale**: *"Trova l'RFC il cui titolo contiene la frase 'Hypertext Transfer Protocol'."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe cercare l'RFC che definisce il protocollo HTTP, sapendo che il titolo esatto contiene questa frase.  
4. **Motivo per cui la query è adatta per il test**:  
   Verifica la capacità del motore di gestire frasi esatte in un campo specifico, distinguendo tra ricerche esatte e parziali.

---

### **Query 3**
1. **Query**: `title:"Simple Mail Transfer Protocol" AND status:"Standard" AND keywords:"email"`  
2. **Linguaggio naturale**: *"Cerca un RFC il cui titolo contenga 'Simple Mail Transfer Protocol', il cui stato sia 'Standard', e che abbia come parola chiave 'email'."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   L'utente potrebbe voler trovare un documento che definisce formalmente l'SMTP (standard ufficiale) e che sia rilevante per l'invio di email.  
4. **Motivo per cui la query è adatta per il test**:  
   Testa l'abilità del motore di combinare condizioni multiple su più campi e di gestire operatori logici complessi.

---

### **Query 4**
1. **Query**: `authors:"Vinton Cerf"`  
2. **Linguaggio naturale**: *"Trova tutti gli RFC scritti da Vinton Cerf."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un ricercatore potrebbe voler esaminare i contributi di Vinton Cerf, uno dei pionieri di Internet, per studiare il suo impatto.  
4. **Motivo per cui la query è adatta per il test**:  
   Verifica la capacità del motore di gestire ricerche specifiche su un autore, anche in un campo con valori potenzialmente ambigui (es. nomi simili).

---

### **Query 5**
1. **Query**: `abstract OR keywords OR content:"networking"`  
2. **Linguaggio naturale**: *"Cerca documenti che contengano la parola 'networking' in abstract, keywords o content."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe voler esplorare tutti gli RFC che trattano il networking, senza sapere a priori dove viene menzionato.  
4. **Motivo per cui la query è adatta per il test**:  
   Testa la ricerca su più campi contemporaneamente, verificando l’abilità del motore di identificare risultati pertinenti in contesti diversi.

---

### **Query 6**
1. **Query**: `status:"Informational"`  
2. **Linguaggio naturale**: *"Trova tutti gli RFC il cui stato è 'Informational'."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe voler consultare RFC "Informational" per ottenere linee guida, raccomandazioni o informazioni generali.  
4. **Motivo per cui la query è adatta per il test**:  
   Verifica se il motore riesce a filtrare documenti basati su uno stato categoriale, utile per ricerche più mirate.

---

### **Query 7**
1. **Query**: `content:"data"`  
2. **Linguaggio naturale**: *"Trova tutti i documenti che contengono la parola 'data' nel contenuto."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   L'utente potrebbe cercare informazioni sui dati in generale, esplorando come il termine viene usato in vari RFC.  
4. **Motivo per cui la query è adatta per il test**:  
   Permette di valutare la gestione di query generiche e con risultati potenzialmente numerosi, mettendo alla prova il ranking della rilevanza.

---

### **Query 8**
1. **Query**: `keywords:"authentication" AND keywords:"encryption"`  
2. **Linguaggio naturale**: *"Trova documenti che abbiano 'authentication' e 'encryption' tra le parole chiave."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente interessato alla sicurezza potrebbe voler trovare RFC che trattano entrambi gli aspetti, per approfondire argomenti correlati.  
4. **Motivo per cui la query è adatta per il test**:  
   Testa la gestione di query con condizioni multiple nello stesso campo e il supporto per operatori AND.

---

### **Query 9**
1. **Query**: `content:"end-to-end encryption"`  
2. **Linguaggio naturale**: *"Trova documenti che contengano la frase esatta 'end-to-end encryption' nel contenuto."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe voler approfondire come gli RFC trattano la crittografia end-to-end, cercando documenti pertinenti.  
4. **Motivo per cui la query è adatta per il test**:  
   Valuta la capacità del motore di distinguere tra frasi esatte e ricerche per singole parole.

---

### **Query 10**
1. **Query**: `content:"transport protocol" AND authors:"Jon Postel" AND status:"Historic"`  
2. **Linguaggio naturale**: *"Trova un documento che contenga 'transport protocol' nel contenuto, scritto da Jon Postel e il cui stato sia 'Historic'."*  
3. **Motivo per cui la query può essere utile per l'utente**:  
   Un utente potrebbe voler studiare documenti storici sui protocolli di trasporto, scritti da una figura chiave come Jon Postel.  
4. **Motivo per cui la query è adatta per il test**:  
   Testa la capacità del motore di elaborare query complesse che combinano più campi e condizioni specifiche.
```