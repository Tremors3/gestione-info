from whoosh.scoring import Weighting
from whoosh.qparser import QueryParser
from whoosh import index

class CustomScorer(Weighting):
    def score(self, searcher, fieldname, text, docnum, weight, QTF=2):
        # Ottieni il valore del campo "value" (popolazione)
        population = searcher.stored_fields(docnum).get("value", 0)
        # Combina frequenza (TF) con popolazione
        return 1 * (population / 1000000)

ix = index.open_dir("index_dir")

# Usa il ranking personalizzato
with ix.searcher(weighting=CustomScorer()) as searcher:
    parser = QueryParser("country_name", ix.schema)
    query = parser.parse("China AND year:2007")
    results = searcher.search(query, limit=None)

    # Stampa i risultati con ranking personalizzato
    for result in results:
        print(dict(result), "Score:", result.score)
