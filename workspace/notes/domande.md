
SITEMAP
https://www.scrapingbee.com/blog/how-to-find-all-urls-on-a-domains-website-multiple-methods/

PRESENTAZIONE DI DANIELE
https://docs.google.com/presentation/d/1E_2JCJo_qjcJumgJIEgiAoG7QP-wKdAQcSZL_HtwL9E/edit#slide=id.g71c787723f_0_33

----------------------------------------------------------------------------------------------------------------

DOMANDE

DOMANDA 1
Prof, il progetto quest'anno è più incentrato sullo sviluppo di funzionalità del search engine (keyword search, ricerca esatta, ranged query, filtraggio di categorie (es. gioco va su linux / va su widows) ...)
    oppure
è più incentrato sul banchmarking

DOMANDA 2
Per QUALITA' nelle slide di presentazione del progetto, intende quantità di features?
Anche se non intende features, può comunque anzare il voto implementarne alcune (keyword search, ricerca esatta, ranged query, ...)

DOMANDA 3
Cosa intende la prof per perculiarità dei search engine?
    Vuole che implementiamo delle features peculiari diverse per ogni search engine.
    Oppure vuole tre search engine con le stesse features per confrontarli meglio (confrontare i sistemi (whoosh, postgress, pylucene)).
FEATURES o NON FEATURES?

DOMANDA 4
E' meglio che facciamo il nostro preprocessing con nltk (o altri tools), oppure utilizziamo il preprocessing offerto da pylucene, whoosh e postresql?

----------------------------------------------------------------------------------------------------------------

DECISIONI

1. CHE DATASET UTILIZZARE?
    - SCELTA DI UN DATASET CON METADATI (es gioco steam) + SCRAPING DI REVIEWS (es critiche su metacritic).
    - DATASET=METADATI + SCRAPING INFORMAZIONI PER FARE RANKING.
2. CHE USER NEEDS ABBIAMO.
3. SCELTA DELLE FEATURES DA IMPLEMENTARE (se richieste dalla prof).

PROCEDIMENTO SVILUPPO

1. SCELTA DATASET (kaggle, huggin face)
2. SVILUPPO TUTTI ASSIEME CON WHOOSH DEL PRIMO SEARCH ENGINE (con anche funzionalità di query language)
3. PORTING SUGLI ALTRI SISTEMI (sviluppo funzionalità specifiche per questi altri sistemi + aggiunta di quelle già fatte su whoosh)
    POSTGRESS --> QUERY ESATTE
    ALTRI --> NO
4. BENCHMARKING

Implementiamo prima il 

----------------------------------------------------------------------------------------------------------------------------------------------------------------





