from org.apache.lucene.search import BooleanQuery, BooleanClause
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.util import Version

class MyPyLucene:
    
    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            MyPyLucene.create_indexes()
        
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        
        fsDir = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        searcher = IndexSearcher(DirectoryReader.open(fsDir))
        
        analyzer = StandardAnalyzer()

        # Crea un BooleanQuery per combinare le query su più campi
        boolean_query = BooleanQuery.Builder()

        # Crea il parser per i vari campi
        parser_title = QueryParser("title", analyzer)
        parser_abstract = QueryParser("abstract", analyzer)
        parser_content = QueryParser("content", analyzer)

        # Aggiungi le query sui vari campi
        query_title = parser_title.parse(data["ricerca_principale"])
        query_abstract = parser_abstract.parse(data["ricerca_principale"])
        query_content = parser_content.parse(data["ricerca_principale"])

        # Combina le query usando l'operatore AND per tutti i campi
        boolean_query.add(query_title, BooleanClause.Occur.SHOULD)  # Aggiungi la query per il titolo
        boolean_query.add(query_abstract, BooleanClause.Occur.SHOULD)  # Aggiungi la query per l'abstract
        boolean_query.add(query_content, BooleanClause.Occur.SHOULD)  # Aggiungi la query per il contenuto

        # Esegui la ricerca combinata
        scoreDocs = searcher.search(boolean_query.build(), data.get("size", 50)).scoreDocs
        
        print(f"Numero di risultati trovati: {len(scoreDocs)}")  # Verifica il numero di risultati
        
        # Restituisci i risultati
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print(f"Title: {doc.get('title')}, Abstract: {doc.get('abstract')}")
        
        return len(scoreDocs)

# Test
data = {
    "ricerca_principale": "protocol",  # La parola da cercare
    "size": 50
}
results = MyPyLucene._execute_query(data)
print(f"Numero di risultati: {results}")