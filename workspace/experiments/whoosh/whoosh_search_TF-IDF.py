from whoosh.query import Term, TermRange, Not, Wildcard
from whoosh.qparser import QueryParser
from whoosh.scoring import TF_IDF
from whoosh import index
import time

# Ranking basato sul TF-IDF (Term Frequency-Inverse Document Frequency)

ix = index.open_dir("index_dir")

# Imposta il modello di ranking TF-IDF
with ix.searcher(weighting=TF_IDF()) as searcher:
    #parser = QueryParser("country_name", ix.schema)
    #query = parser.parse("China AND year:2010")
    start_time = time.time()

    query = Wildcard("content","*protoc*")
    date_filter_1 = TermRange("date", "1996-02", "1997")
    date_filter_2 = Not(Term("date", "1996-04"))

    query = query & date_filter_1
    results = searcher.search(query, limit=None)
    end_time = time.time()
    
    # Stampa i risultati ordinati per punteggio TF-IDF
    for r in results:
        print(f"{r['date']}   Score: {r.score}")

    print("\nModello di ranking: TF-IDF")
    print(f"Query: {query}")
    print(f"Tempo: {end_time - start_time:.6f} secondi")