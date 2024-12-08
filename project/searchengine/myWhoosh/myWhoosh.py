import os, json
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED, KEYWORD, DATETIME
from whoosh.qparser import QueryParser, GtLtPlugin

class MyWhoosh:
    
    DATASET_PATH = os.path.join("project", "searchengine", "dataset", "dataset.json")
    INDEX_DIR_PATH = os.path.join("project", "searchengine", "myWhoosh", "index_dir")
    
    @staticmethod
    def _create_index_dir():
        """ Funzione che controlla se l'indice è già stato creato, se no lo crea. """
        
        # Crea la cartella dove sarranno messi gli indici
        os.mkdir(MyWhoosh.INDEX_DIR_PATH)
    
        with open(MyWhoosh.DATASET_PATH, mode="r", encoding='utf-8') as f:
            doc = json.load(f)

        schema = Schema(
            number    = ID(stored=True, unique=True),
            files     = STORED,
            title     = TEXT(stored=True),
            authors   = TEXT(stored=True),
            date      = STORED,
            more_info = STORED,
            status    = TEXT(stored=True),
            abstract  = TEXT(stored=True),
            keywords  = KEYWORD(commas=True),
            content   = TEXT
        )

        ix = index.create_in(MyWhoosh.INDEX_DIR_PATH, schema)
        writer = ix.writer()

        for d in doc:
            writer.add_document(
                number    = d["Number"],
                files     = d["Files"],
                title     = d["Title"],
                authors   = d["Authors"],
                date      = d["Date"],
                more_info = d["More Info"],
                status    = d["Status"],
                abstract  = d["Abstract"],
                keywords  = d["Keywords"],
                content   = d["Content"]
            )

        writer.commit()
        
    @staticmethod
    def _results_to_json(results):
        """Converte i risultati di Whoosh in un formato JSON-friendly."""
        
        results_list = []
        for result in results:
            
            result = dict(result)
            
            # Aggunta alla lista
            results_list.append(result)
        
        return json.dumps(results_list)  

    @staticmethod
    def execute_query(data: dict):
        """ Funzione che esegue una query """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyWhoosh.INDEX_DIR_PATH):
            MyWhoosh._create_index_dir()
        
        ### Esecuzione della query ###
        
        # Apertura dell'indice
        ix = index.open_dir(MyWhoosh.INDEX_DIR_PATH)

        # Corpo della query principale
        query = data["ricerca_principale"]

        # Logica dei Termini di Ricerca
        for t in data["terms"]:
            
            # Recupero dei valori del termine
            term = t["term"]
            op = t["operator"]
            field = t["field"].lower()

            # Traduzione dell'operatore NOT in AND NOT
            if op == "NOT":
                op = "AND NOT"

            # Costruzione della query (append)
            query = f'{query} {op} {field}:"{term}"'

        # Parserizza la Query
        query = QueryParser("content", ix.schema).parse(query)
        
        # Estrazione dei risultati
        with ix.searcher() as searcher:
            
            # Ottenimento dei rislutati
            results = searcher.search(query, limit=data.get("size"))
            
            # Formattazione dei Risultati
            results = MyWhoosh._results_to_json(results)
               
        return results

def process(query: dict):
    return MyWhoosh.execute_query(query)

if __name__ == "__main__":
    #process()
    pass