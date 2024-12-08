### [idea] BENCHMARK

PROPOSTA LLM PER VERIFICARE LA CORRETTEZZA DEI DATI SULLA RILEVANZA (GIA' CALCOLATA) DEI DOCUMENTI DEL BENCHMARK
Una voltal eseguito lo script di creazione del benchmark otteniamo una lista di documenti con relativa rilevanza ad una data query. Invece di essere noi manualmente a fare un controllo sull'assegnazione della "Rilevanza Normalizzata Arrotondata" lo facciamo fare ad una LLVM addestrata?

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

### [da_finire(parte_whoosh)] MODIFICARE ALCUNE COSE DEI TERMINI DI RICERCA

Rimuoviamo l'operatore OR perchè introduce molta logica difficile da gestire tra i diversi motori di Ricerca.

Rnominiamo "AND" ad "IN", mentre rinominiamo "NOT" ad "NOT IN"; in questo modo è più chiaro che non ci stiamo riferendo agli operatori AND e OR ma al fatto che all'interno dei campo i termini devono esserci o no in modo esatto. E' un podo per essere più chiari e precisi.

# COSE DA FARE

### [da_fare] QUANDO VENGONO CREATI GLI INVERTED INDEX dei SEARCH ENGINE ?

- [ ] Gli indici di tutti i modelli di ranking e dei vari sistemi devono essere creati subito dopo il download dei documenti tramite il parser.
      Ogni volta che viene ricreato il dataset devono venir ricreati anche tutti gli indici dei vari sistemi e modelli.

### [da_fare] RIORGANIZZARE DEMO WHOOSH

- [ ] Riorganizzare la demo di whoosh facendo tutti i controlli necessari, mettendo apposto i percorsi, ecc...













