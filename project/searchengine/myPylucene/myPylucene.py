
# https://lucene.apache.org/core/10_0_0/

# #################################################################################################### #

import os, sys, json, shutil
from datetime import datetime

# #################################################################################################### #

import lucene

from java.nio.file import Paths

from org.apache.lucene.util import Version, BytesRef

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import NIOFSDirectory

from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery, TermRangeQuery

# #################################################################################################### #

class MyPyLucene:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(CURRENT_FILE_PATH, "indexes_dir")
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")

    # LIST OF ALL FIELDS IN THE JSON FILE
    FIELDS_LIST = ["number", "files", "title", "authors", "date", "more_info", "status", "abstract", "keywords", "content"]

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyPyLucene.DATASET_FILE_PATH):
            print(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyPyLucene.DATASET_FILE_PATH}\'.")
            sys.exit(1)
        
        # Controllo se la cartella degli indici esiste
        if os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            # Se esiste la elimino
            shutil.rmtree(MyPyLucene.INDEX_DIRECTORY_PATH)
        
        # Creazione della cartella degli indici
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            os.mkdir(MyPyLucene.INDEX_DIRECTORY_PATH)
    
    @staticmethod
    def _write_indexes():
        """ Funzione che scrive gli indici per la ricerca. """    
        
        # Inizializzazione di Lucene
        lucene.initVM(vmargs=['-Djava.awt.headless=True'])
        
        # Apertura della directory
        directory = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        # Creazione dell'analizzatore
        analyzer = StandardAnalyzer()
        
        # Configurazione dell'indice
        config = IndexWriterConfig(analyzer)
        
        # Creazione dell'indice
        writer = IndexWriter(directory, config)
        
        # Apertura del file del dataset
        with open(MyPyLucene.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)

        count=0
        
        for jdoc in documents:

            count += 1

            # Creazione del documento
            doc = Document()
        
            # Campi memorizzati
            doc.add(Field("number",     jdoc["Number"],              StringField.TYPE_STORED))
            doc.add(Field("files",      " ".join(jdoc["Files"]),     TextField.TYPE_STORED))
            doc.add(Field("title",      jdoc["Title"],               TextField.TYPE_STORED))
            doc.add(Field("authors",    " ".join(jdoc["Authors"]),   TextField.TYPE_STORED))
            doc.add(Field("date",       jdoc["Date"],                TextField.TYPE_STORED))
            doc.add(Field("more_info",  jdoc["More Info"],           StringField.TYPE_STORED))
            doc.add(Field("status",     jdoc["Status"],              StringField.TYPE_STORED))
            doc.add(Field("abstract",   jdoc["Abstract"],            TextField.TYPE_STORED))
            
            # Campi non memorizzati
            doc.add(Field("keywords",   " ".join(jdoc["Keywords"]),  TextField.TYPE_NOT_STORED))
            doc.add(Field("content",    jdoc["Content"],             TextField.TYPE_NOT_STORED))
            
            # Aggiunta del documento all'indice
            writer.addDocument(doc)
        
        # Commit e chiusura del writer
        writer.commit()
        writer.close()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        MyPyLucene._prepare_folders_and_files()
        MyPyLucene._write_indexes()

    # #################################################################################################### #
    
    @staticmethod
    def _results_to_json(searcher, scoreDocs):
        """Converte i risultati di Pylucene in un formato JSON-friendly."""
        
        results_list = []
        
        for scoreDoc in scoreDocs:

            doc = searcher.doc(scoreDoc.doc)

            result = {}
            
            # Campi da estrarre
            for field_name in ["number", "files", "title", "authors", "date", "more_info", "status", "abstract"]:
                
                field_value = doc.get(field_name)
                
                if field_value: result[field_name] = field_value

            results_list.append(result)
        
        return results_list  

    @staticmethod
    def _filter_results_by_date(data, documents):
        """Filtra i risultati precedentemente ottenuti per data."""

        date_value = data.get("dates", "").strip().upper()

        # Nel caso non ci sia bisogno di effettuare filtraggi, 
        # restutuzione di tutti i documenti
        if date_value == "ALL_DATES": return documents
        
        results = []
        
        for doc in documents:
            
            # Filtraggio per anno specifico (SPECIFIC_YEAR)
            if date_value == "SPECIFIC_YEAR":
                
                specific_year = data.get("date_year", "").split('-')[0] if data.get("date_year") else None
                document_year = doc.get("date", "").split('-')[0] if doc.get("date") else None
                
                # Verifica che la data del documenti corrisponda a quella filtrata
                if specific_year and document_year and specific_year == document_year:
                    results.append(doc)
            
            # Filtraggio per intervallo di date (DATE_RANGE)
            elif date_value == "DATE_RANGE":
                
                from_date_str = data.get("date_from_date")
                to_date_str = data.get("date_to_date")
                
                if from_date_str and to_date_str:
                    
                    try:
                        
                        # Parsing delle date
                        doc_date = datetime.strptime(doc.get("date", ""), "%Y-%m")
                        from_date = datetime.strptime(from_date_str, "%Y-%m")
                        to_date = datetime.strptime(to_date_str, "%Y-%m")
                        
                        # Verifica che la data del documento sia nel range
                        if from_date <= doc_date <= to_date:
                            results.append(doc)
                    
                    except Exception: pass
        
        return results

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            MyPyLucene.create_indexes()
        
        # Inizializzazione di Lucene
        lucene.initVM(vmargs=['-Djava.awt.headless=True'])
        
        # Apertura della directory
        fsDir = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        # Apertura del reader
        reader = DirectoryReader.open(fsDir)
        
        # Apertura del searcher
        searcher = IndexSearcher(reader)
        
        # Creazione dell'analizzatore
        analyzer = StandardAnalyzer()

        # #################################################################################################### #
        
        # QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO
        
        content_query_builder = BooleanQuery.Builder()
        
        parser = QueryParser("content", analyzer)
        
        #parser.setDefaultOperator(QueryParser.Operator.AND)
        
        content_query = parser.parse(data["ricerca_principale"])
        
        # #################################################################################################### #
        
        # RICERCA SU PIU' CAMPI
        
        ## Enum BooleanClause.Occur.
        ## https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/BooleanClause.Occur.html
        # FILTER - Like MUST except that these clauses do not participate in scoring.
        # MUST - Use this operator for clauses that must appear in the matching documents.
        # MUST_NOT - Use this operator for clauses that must not appear in the matching documents.
        # SHOULD - Use this operator for clauses that should appear in the matching documents.
        
        run_terms_search = data["terms"]
        
        if run_terms_search:
            
            # Crea un BooleanQuery per combinare le query sullo stato
            terms_query_builder = BooleanQuery.Builder()
        
            for term_data in data["terms"]:
                
                # Recupero dei valori del termine
                term = term_data["term"]
                op = term_data["operator"].strip().upper()
                field = term_data["field"].strip().upper()
                
                # Mappatura tra chiavi e operatori
                operator_mapping = {
                    "AND": BooleanClause.Occur.MUST,
                    "NOT": BooleanClause.Occur.MUST_NOT,
                    "OR": BooleanClause.Occur.SHOULD
                }
                
                # Imposta l'operatore
                op = operator_mapping.get(op, BooleanClause.Occur.SHOULD)
                
                # Mappatura tra chiavi e campi
                field_mapping = {
                    "TITLE": "title",
                    "DESCRIPTION": "abstract",
                    "KEYWORDS": "keywords"
                }
                
                # Imposta il campo
                field = field_mapping.get(field, "abstract")
                
                # Crea il parser per il campo
                parser = QueryParser(field, analyzer)
                
                # Costruzione della query
                query = parser.parse(term)
                
                # Aggiungi la query al BooleanQuery
                terms_query_builder.add(query, op)
            
            terms_query = terms_query_builder.build()
        
        # #################################################################################################### #
        
        # RICERCA PER STATO
        
        # TermQuery - Una TermQuery è una query semplice e diretta in Lucene che cerca un termine esatto in un campo specifico.
        # QueryParser - Il QueryParser è uno strumento di Lucene che permette di analizzare una stringa di query scritta in linguaggio naturale o quasi, e convertirla in una query Lucene. È più potente e versatile, ma richiede una stringa di input come query.
        
        run_status_search = any(data[key] for key in ["standard_track", "best_current_practice", "informational", "experimental", "historic"])
        
        if run_status_search:
            
            # Crea un BooleanQuery per combinare le query sullo stato
            status_query_builder = BooleanQuery.Builder()

            # Mappatura tra chiavi e stati
            status_mapping = {
                "best_current_practice": "Best Current Practice",
                "informational": "Informational",
                "experimental": "Experimental",
                "historic": "Historic",
            }

            # Aggiungi stati specifici per "standard_track"
            if data["standard_track"]:
                
                value = data["standard_track_value"].strip().upper()
                
                standard_track_mapping = {
                    "PROPOSED_STANDARD": "Proposed Standard",
                    "DRAFT_STANDARD": "Draft Standard",
                    "INTERNET_STANDARD": "Internet Standard",
                }
                
                if value in standard_track_mapping:
                    status_query_builder.add(TermQuery(Term("status", standard_track_mapping[value])), BooleanClause.Occur.SHOULD)

            # Aggiungi gli altri stati mappati
            for key, status in status_mapping.items():
                if data[key]:
                    status_query_builder.add(TermQuery(Term("status", status)), BooleanClause.Occur.SHOULD)
        
            status_query = status_query_builder.build()
        
        # #################################################################################################### #
        
        # RICERCA PER DATA --- IMPLEMENTATA IN POST-PROCESSING
        
        # #################################################################################################### #
        
        # COSTRUZIONE DELLA QUERY FINALE
        
        final_query_builder = BooleanQuery.Builder()
        final_query_builder.add(content_query, BooleanClause.Occur.MUST)
        if run_terms_search: final_query_builder.add(terms_query, BooleanClause.Occur.MUST)
        if run_status_search: final_query_builder.add(status_query, BooleanClause.Occur.MUST)
        #if run_date_search: final_query_builder.add(date_query, BooleanClause.Occur.MUST)
        
        # #################################################################################################### #
        
        # ESTRAZIONE DEI RISULTATI
        
        # Estrazione
        scoreDocs = searcher.search(final_query_builder.build(), data.get("size", 25)).scoreDocs
        
        # Logging
        print(f"Numero di risultati trovati: {len(scoreDocs)}")  
        
        # Formattazione
        results = MyPyLucene._results_to_json(searcher, scoreDocs)
        
        # #################################################################################################### #
        
        # OPERAZIONI POST-PROCESSING
        
        results = MyPyLucene._filter_results_by_date(data, results)
        
        # #################################################################################################### #
        
        return results

    # #################################################################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPyLucene._execute_query(query)

# #################################################################################################### #

def test_indexes_creation():
    MyPyLucene.create_indexes()

def test_query_execution():
    results = MyPyLucene.process({
        "ricerca_principale":"QUIC Protocol",
        "spelling_correction":False,
        "synonims":False,
        "search_engine":"PYLUCENE",
        "standard_track":True,
        "best_current_practice":False,
        "informational":False,
        "experimental":False,
        "historic":False,
        "standard_track_value":"PROPOSED_STANDARD",
        "date_year":"2021",
        "date_from_date":"2021-04",
        "date_to_date":"2021-06",
        "dates":"DATE_RANGE",
        "terms":[
            {
                "operator":"AND",
                "term":"QUIC",
                "field":"TITLE"
            },
            {
                "operator":"AND",
                "term":"document",
                "field":"DESCRIPTION"
            },
            {
                "operator":"NOT",
                "term":"network",
                "field":"KEYWORDS"
            }
        ],
        "abstracts":"True",
        "size":25
    })
    
    for doc in results: print(doc, '\n')

if __name__ == "__main__":
    #test_indexes_creation()
    test_query_execution()
    pass