from whoosh.query import Term, TermRange, Not, Prefix, Wildcard
from whoosh.qparser import QueryParser
from whoosh import index
import time

# Ranking basato sul BM25F, che è il default ranking model di Whoosh
# Non è quindi necessario configurarlo esplicitamente.

ix = index.open_dir("index_dir")

with ix.searcher() as searcher:
    #parser = QueryParser("country_name", ix.schema)
    #query = parser.parse("China AND year:2010")
    start_time = time.time()

    query = Wildcard("content","*protoc*")
    date_filter_1 = TermRange("date", "1996-02", "1997")
    date_filter_2 = Not(Term("date", "1996-04"))

    query = query & date_filter_1
    results = searcher.search(query, limit=None)
    end_time = time.time()
    
    # Stampa i risultati ordinati per punteggio BM25F;
    # Rappresenta la rilevanza stimata di un documento rispetto alla query
    for r in results:
        print(f"{r['date']}   Score: {r.score}")
    
    print("\nModello di ranking: BM25F")
    print(f"Query: {query}")
    print(f"Tempo: {end_time - start_time:.6f} secondi")