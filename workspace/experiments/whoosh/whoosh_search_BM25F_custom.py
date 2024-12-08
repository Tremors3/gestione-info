from whoosh.qparser import QueryParser
from whoosh.scoring import BM25F
from whoosh import index

# Parametri personalizzati:
# B   = bilancia l'importanza della lunghezza del documento
# K1  = sensibilità alla frequenza
bm25f_custom = BM25F(B=1, K1=0.5)
ix = index.open_dir("index_dir")

with ix.searcher(weighting=bm25f_custom) as searcher:
    parser = QueryParser("country_name", ix.schema)
    query = parser.parse("China AND year:2010")
    results = searcher.search(query, limit=None)

    # Stampa i risultati ordinati per punteggio BM25F personalizzato
    for r in results:
        print(dict(r), "Score:", r.score)