import json
from whoosh import index
from whoosh.qparser import QueryParser, GtLtPlugin
#from whoosh.query import Term, Phrase, And, Or, Not
#from whoosh.analysis import RegexTokenizer, LowercaseFilter

ix = index.open_dir("index_dir")

with open("query.json", "r") as f:
    data = json.load(f)

query = data["ricerca_principale"]

for t in data["terms"]:
    term = t["term"]
    op = t["operator"]
    field = t["field"].lower()

    if op == "NOT":
        op = "AND NOT"

    query = f'{query} {op} {field}:"{term}"'

query = QueryParser("content", ix.schema).parse(query)
print(query)

with ix.searcher() as searcher:
    results = searcher.search(query, limit=3)

    print(len(results), "risultato/i")
    for r in results:
        print(r["number"])

#print("Query: ", query)

def test():
    #analyzer = RegexTokenizer()

    #RegexTokenizer(title_str)
    #normalized_terms = [token.text for token in RegexTokenizer()(title_str)]
    #title_str = title_str.split()
    #term2 = Phrase("title", normalized_terms)
    #query = QueryParser("Content", ix.schema).parse("consensus")

    title_parser = QueryParser("title", ix.schema)
    title_str = "Content Delivery Network Interconnection (CDNI) Metadata"
    kw_str = "IPv6 Address Synthesis"

    # Ricerca di una FRASE nel campo "title":
    # Query: (title:"content delivery network interconnection cdni metadata").
    # Restituisce un risultato se il titolo contiene la frase specificata.
    ricerca_frase_titolo = title_parser.parse(f'"{title_str}"')

    # Ricerca di TERMINI (di cui è composta la stringa "title_str") nel campo "title":
    # Query: (title:content AND title:delivery AND title:network AND title:interconnection AND title:cdni AND title:metadata).
    # Restituisce un risultato se il titolo contiene TUTTI i termini specificati.
    ricerca_termini_titolo = title_parser.parse(title_str)

    query_str = f'OR title:"{title_str}" NOT keywords:"{kw_str}" AND NOT title:"delivery"'


    ricerca_kw = QueryParser("keywords", ix.schema).parse(f'{kw_str}')
    #query = QueryParser("content", ix.schema).parse(f"persons {query_str}")

    test_str = """
                title:"Simple Mail Transfer Protocol" AND status:"Standard" OR keywords:"email" OR keywords:"geoblocking"
               """
    
    test_str = 'number:>=8990'
    
    parser = QueryParser("content", ix.schema)
    parser.add_plugin(GtLtPlugin)
    query = parser.parse(test_str)

    #query = And([Not(query), ricerca_frase_titolo])
    #query = Or([query, ricerca_kw])

    print("\nTestQ:", query)

    with ix.searcher() as searcher:
        results = searcher.search(query, limit=3)
        print(len(results), "risultato/i")
        for r in results:
            print(r["number"])

test()