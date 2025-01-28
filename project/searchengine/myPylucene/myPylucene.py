
# https://lucene.apache.org/core/10_0_0/

# Importazione delle librerie standard
import os, sys, json, shutil
from datetime import datetime

# Importazione di Lucene e altre librerie necessarie
import lucene
from java.nio.file import Paths

# Lucene: Utilità e Classi per la gestione dell'indice
from org.apache.lucene.util import Version, BytesRef
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import NIOFSDirectory

# Lucene: Classi per la lettura dell'indice e la ricerca
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery, TermRangeQuery

# ########################################################### #

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
        
        # Inizializzazione di Lucene (configurazione per eseguire senza interfaccia grafica)
        lucene.initVM(vmargs=['-Djava.awt.headless=True'])

        # Apertura della directory dell'indice (in modalità lettura/scrittura)
        directory = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))

        # Creazione dell'analizzatore standard per il testo
        analyzer = StandardAnalyzer()

        # Configurazione del writer per l'indice
        config = IndexWriterConfig(analyzer)

        # Creazione del writer per l'indice
        writer = IndexWriter(directory, config)

        # Apertura e lettura del dataset da file JSON
        with open(MyPyLucene.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)

        # Contatore per il numero di documenti processati
        count = 0

        # Iterazione su ciascun documento del dataset
        for jdoc in documents:
            count += 1
            
            # Creazione di un nuovo documento Lucene
            doc = Document()
            
            # Aggiunta dei campi memorizzati al documento
            doc.add(Field("number",    jdoc["Number"],              StringField.TYPE_STORED))
            doc.add(Field("title",     jdoc["Title"],               TextField.TYPE_STORED))
            doc.add(Field("authors",   " ".join(jdoc["Authors"]),   TextField.TYPE_STORED))
            doc.add(Field("date",      jdoc["Date"],                TextField.TYPE_STORED))
            doc.add(Field("status",    jdoc["Status"],              StringField.TYPE_STORED))
            doc.add(Field("abstract",  jdoc["Abstract"],            TextField.TYPE_STORED))
            doc.add(Field("keywords",  " ".join(jdoc["Keywords"]),  TextField.TYPE_STORED))
            doc.add(Field("more_info", jdoc["More Info"],           StringField.TYPE_STORED))
            doc.add(Field("files",     " ".join(jdoc["Files"]),     TextField.TYPE_STORED))
            
            # Aggiunta di campi non memorizzati (contenuto)
            doc.add(Field("content",   jdoc["Content"],             TextField.TYPE_NOT_STORED))
            
            # Aggiunta del documento all'indice
            writer.addDocument(doc)

        # Completamento delle operazioni di scrittura e chiusura del writer
        writer.commit()
        writer.close()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        MyPyLucene._prepare_folders_and_files()
        MyPyLucene._write_indexes()

    # ########################################################### #
    
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

        # Estrazione del valore per il filtro delle date
        date_value = data.get("dates", "").strip().upper()

        # Nel caso in cui non sia necessario applicare alcun filtro sulle date,
        # restituiamo tutti i documenti
        if date_value == "ALL_DATES":
            return documents

        # Lista per memorizzare i risultati filtrati
        results = []

        # Iterazione su tutti i documenti per applicare i filtri sulle date
        for doc in documents:

            # Filtro per anno specifico (SPECIFIC_YEAR)
            if date_value == "SPECIFIC_YEAR" and data.get("date_year"):
                
                specific_year = data.get("date_year", 2000)  # Anno specificato per il filtro
                document_year = doc.get("date", "").split('-')[0] if doc.get("date") else None  # Estrazione dell'anno dal documento
                
                # Verifica che l'anno del documento corrisponda all'anno specificato nel filtro
                if specific_year and document_year and specific_year == document_year:
                    results.append(doc)

            # Filtro per intervallo di date (DATE_RANGE)
            elif date_value == "DATE_RANGE" and data.get("date_from_date") and data.get("date_to_date"):
                
                from_date_str = data.get("date_from_date")  # Data di inizio dell'intervallo
                to_date_str = data.get("date_to_date")      # Data di fine dell'intervallo
                
                if from_date_str and to_date_str:
                    try:
                        # Parsing delle date di documento e intervallo
                        doc_date = datetime.strptime(doc.get("date", ""), "%Y-%m")
                        from_date = datetime.strptime(from_date_str, "%Y-%m")
                        to_date = datetime.strptime(to_date_str, "%Y-%m")
                        
                        # Verifica se la data del documento è all'interno dell'intervallo specificato
                        if from_date <= doc_date <= to_date:
                            results.append(doc)
                    
                    except Exception:
                        pass

        # Restituzione dei documenti che soddisfano i criteri di data
        return results

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # ########################################################### #
        # INIZIALIZZAZIONE PARAMETRI
        # ########################################################### #

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

        # ########################################################### #
        # QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO
        # ########################################################### #

        # Creazione di una query booleana per la ricerca nel campo "content"
        content_query_builder = BooleanQuery.Builder()

        # Creazione di un parser per la ricerca nel campo "content"
        parser = QueryParser("content", analyzer)

        # Impostazione dell'operatore di default per il parser (AND tra i termini)
        # parser.setDefaultOperator(QueryParser.Operator.AND)

        # Parsing della query principale fornita dall'utente
        content_query = parser.parse(data["ricerca_principale"])
        
        # ########################################################### #
        # RICERCA SU PIU' CAMPI - CREAZIONE DI UNA QUERY BOOLEANA COMBINATA
        # ########################################################### #
        
        ## Enum BooleanClause.Occur.
        ## https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/BooleanClause.Occur.html
        # FILTER - Like MUST except that these clauses do not participate in scoring.
        # MUST - Use this operator for clauses that must appear in the matching documents.
        # MUST_NOT - Use this operator for clauses that must not appear in the matching documents.
        # SHOULD - Use this operator for clauses that should appear in the matching documents.

        # Verifica se sono presenti termini per la ricerca
        run_terms_search = data["terms"]

        # Se ci sono termini da cercare, esegui la ricerca su più campi
        if run_terms_search:
            
            # Inizializzazione di un costruttore per la query booleana
            terms_query_builder = BooleanQuery.Builder()

            # Itera attraverso ogni termine di ricerca
            for term_data in data["terms"]:
                
                # Recupero dei dettagli del termine
                term = term_data["term"]
                operator = term_data["operator"].strip().upper()  # Operatore logico (AND, NOT, OR)
                field = term_data["field"].strip().upper()       # Campo su cui cercare

                # Mappatura tra operatori di ricerca e le corrispondenti clausole di Lucene
                operator_mapping = {
                    "AND": BooleanClause.Occur.MUST,     # Clausola che deve essere soddisfatta
                    "NOT": BooleanClause.Occur.MUST_NOT, # Clausola che non deve essere soddisfatta
                    "OR": BooleanClause.Occur.SHOULD     # Clausola che può essere soddisfatta
                }

                # Imposta l'operatore di ricerca
                op = operator_mapping.get(operator, BooleanClause.Occur.SHOULD)  # Default è SHOULD

                # Mappatura tra chiavi e nomi dei campi nel documento
                field_mapping = {
                    "TITLE": "title",           # Titolo
                    "DESCRIPTION": "abstract",  # Abstract o descrizione
                    "KEYWORDS": "keywords"      # Parole chiave
                }

                # Imposta il campo di ricerca
                field = field_mapping.get(field, "abstract")  # Se il campo non è trovato, usa "abstract"

                # Crea il parser per il campo specificato
                parser = QueryParser(field, analyzer)
                
                # Costruzione della query per il termine
                query = parser.parse(term)
                
                # Aggiungi la query al costruttore della query booleana con l'operatore specificato
                terms_query_builder.add(query, op)

            # Completamento della costruzione della query booleana
            terms_query = terms_query_builder.build()
        
        # ########################################################### #
        # RICERCA PER STATO - CREAZIONE DI UNA QUERY PER LO STATO DEI DOCUMENTI
        # ########################################################### #

        # TermQuery - Una TermQuery è una query semplice e diretta in Lucene che cerca un termine esatto in un campo specifico.
        # QueryParser - Il QueryParser è uno strumento di Lucene che permette di analizzare una stringa di query scritta in linguaggio naturale o quasi, e convertirla in una query Lucene. È più potente e versatile, ma richiede una stringa di input come query.
        
        # Verifica se ci sono i parametri per la ricerca dello stato
        run_status_search = any(data[key] for key in [
            "standard_track", "best_current_practice", "informational", "experimental", "historic"
        ])

        # Se sono presenti parametri di stato, esegui la ricerca
        if run_status_search:
            
            # Crea un costruttore per la query booleana che combinerà le condizioni di ricerca sugli stati
            status_query_builder = BooleanQuery.Builder()

            # Mappatura tra i parametri di stato e i valori di stato
            status_mapping = {
                "best_current_practice": "Best Current Practice",
                "informational": "Informational",
                "experimental": "Experimental",
                "historic": "Historic",
            }

            # Verifica e aggiungi lo stato specifico per "standard_track"
            if data["standard_track"]:
                
                # Estrai il valore specificato per "standard_track" e convertilo in maiuscolo
                value = data["standard_track_value"].strip().upper()
                
                # Mappatura dei valori dello "standard_track"
                standard_track_mapping = {
                    "PROPOSED_STANDARD": "Proposed Standard",
                    "DRAFT_STANDARD": "Draft Standard",
                    "INTERNET_STANDARD": "Internet Standard",
                }
                
                # Se il valore specificato esiste nella mappatura, aggiungi la query per lo stato
                if value in standard_track_mapping:
                    status_query_builder.add(
                        TermQuery(Term("status", standard_track_mapping[value])), 
                        BooleanClause.Occur.SHOULD
                    )

            # Aggiungi gli altri stati mappati (Best Current Practice, Informational, Experimental, Historic)
            for key, status in status_mapping.items():
                if data[key]:
                    status_query_builder.add(
                        TermQuery(Term("status", status)),
                        BooleanClause.Occur.SHOULD
                    )
            
            # Costruzione finale della query booleana per lo stato
            status_query = status_query_builder.build()
        
        # ########################################################### #
        # COSTRUZIONE DELLA QUERY FINALE - COMBINAZIONE DELLE QUERY INDIVIDUALI
        # ########################################################### #

        # Crea il costruttore per la query booleana finale che combinerà tutte le query (content, terms, status)
        final_query_builder = BooleanQuery.Builder()

        # Aggiungi la query sul contenuto del documento, che è obbligatoria (MUST)
        final_query_builder.add(content_query, BooleanClause.Occur.MUST)

        # Se è stato richiesto un filtro sui termini, aggiungi la query, obbligatoria (MUST)
        if run_terms_search:
            final_query_builder.add(terms_query, BooleanClause.Occur.MUST)

        # Se è stato richiesto un filtro sullo stato, aggiungi la query, obbligatoria (MUST)
        if run_status_search:
            final_query_builder.add(status_query, BooleanClause.Occur.MUST)

        # Se è stato richiesto un filtro sulla data, aggiungi la query, obbligatoria (MUST)
        #if run_date_search: final_query_builder.add(date_query, BooleanClause.Occur.MUST)
        
        # ########################################################### #
        # ESTRAZIONE DEI RISULTATI - ESECUZIONE DELLA RICERCA E FORMATTAZIONE DEI RISULTATI
        # ########################################################### #

        # Esegui la ricerca con la query finale costruita e limita il numero di risultati
        # "size" definisce il limite massimo dei risultati da restituire (default 25)
        scoreDocs = searcher.search(final_query_builder.build(), data.get("size", 25)).scoreDocs

        # Log del numero di risultati trovati, utile per il debug o per monitorare le performance
        print(f"Numero di risultati trovati: {len(scoreDocs)}")  

        # Formatta i risultati in un formato leggibile (ad esempio JSON) per la restituzione
        # La funzione _results_to_json converte i documenti risultanti in un formato strutturato
        results = MyPyLucene._results_to_json(searcher, scoreDocs)
        
        # ########################################################### #
        # FILTRAGGIO PER DATA --- IMPLEMENTATA IN POST-PROCESSING
        # ########################################################### #

        # Filtra i risultati ottenuti per data
        results = MyPyLucene._filter_results_by_date(data, results)
        
        # ########################################################### #
        
        return results

    # ########################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPyLucene._execute_query(query)

# ########################################################### #

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
    #test_query_execution()
    pass