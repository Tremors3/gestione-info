
# https://lucene.apache.org/core/10_0_0/

# Importazione
import os, sys, json, shutil
from datetime import datetime

# Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazione di Lucene e Paths
import lucene
from java.nio.file import Paths

# Classi per gestione dell'indice
from org.apache.lucene.util import Version, BytesRef
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import NIOFSDirectory

# Classi per lettura dell'indice e ricerca
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery, TermRangeQuery

# Import moduli di progetto
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors

# #################################################################################################### #

# Tracciare inizializzazione VM
is_vm_initialized = False

# #################################################################################################### #

class MyPyLucene:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "indexes", "lucene_indexes")
    DATASET_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "dataset", "dataset.json")

    # ################################################## #

    @staticmethod
    def init_lucene_vm():
        """ Funzione che inizializza la VM di PyLucene. """
        global is_vm_initialized
        if not is_vm_initialized:
            try:
                # Inizializzazione di Lucene
                lucene.initVM(vmargs=['-Djava.awt.headless=True']) # senza header (ui)
                is_vm_initialized = True
            except Exception: pass

    @staticmethod
    def attach_lucene_to_thread():
        """
        Attacca il thread corrente alla JVM di Lucene.
        Deve essere chiamato prima di gestire ogni richiesta che utilizza lucene.
        """
        try:
            # Attacca il thread corrente alla JVM di Lucene
            lucene.getVMEnv().attachCurrentThread()
        except Exception: pass

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyPyLucene.DATASET_FILE_PATH):
            raise FileExistsError(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyPyLucene.DATASET_FILE_PATH}\'.")
        
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
        MyPyLucene.init_lucene_vm()

        # Apertura della directory dell'indice
        directory = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))

        # Creazione dell'analizzatore standard
        analyzer = StandardAnalyzer()

        # Configurazione del writer per l'indice
        config = IndexWriterConfig(analyzer)

        # Creazione del writer per l'indice
        writer = IndexWriter(directory, config)

        # Apertura e lettura del dataset da file JSON
        with open(MyPyLucene.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)

        # Definizione della barra di caricamento che viene visualizzata durante l'esecuzione
        with alive_bar(len(documents), title="Indicizzazione dei documenti con PyLucene", spinner="waves", bar=_bar) as bar:

            # Per ciascun documento
            for jdoc in documents:

                bar() # Avanza la barra

                doc = Document() # nuovo documento
                
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

        writer.commit() # Commit
        writer.close()  # Chiusura writer

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        logging.debug("PyLucene: Indicizzazione dei documenti...")
        MyPyLucene._prepare_folders_and_files()
        MyPyLucene._write_indexes()

    # #################################################################################################### #
    
    @staticmethod
    def _results_to_json(searcher, scoreDocs):
        """Converte i risultati in un formato JSON."""
        
        results_list = []
        
        for scoreDoc in scoreDocs:

            doc = searcher.doc(scoreDoc.doc)

            result = {}
            
            # Per ciascun campo da estrarre
            for field_name in ["number", "files", "title", "authors", "date", "more_info", "status", "abstract", "keywords"]:
                
                field_value = doc.get(field_name)
                
                if field_name in ["files", "authors", "keywords"]:
                    field_value = str(field_value).split(sep=' ')
                
                if field_value: result[field_name] = field_value

            results_list.append(result)
        
        return results_list  

    @staticmethod
    def _filter_results_by_date(data, documents):
        """Filtra i risultati precedentemente ottenuti per data."""

        # Opzione selezionata
        date_value = data.get("dates", "").strip().upper()

        # Nel caso in cui non sia necessario 
        # applicare alcun filtro sulle date:
        if date_value == "ALL_DATES":
            # restituiamo tutti i documenti
            return documents

        results = [] # Lista per risultati

        # Iteriamo tutti i documenti
        for doc in documents:

            # Filtro per anno specifico (SPECIFIC_YEAR)
            if date_value == "SPECIFIC_YEAR" and data.get("date_year"):
                
                specific_year = data.get("date_year")
                document_year = doc.get("date", "").split('-')[0] if doc.get("date") else None
                
                # Verifica che l'anno del documento corrisponda all'anno specificato nel filtro
                if specific_year and document_year and specific_year == document_year:
                    results.append(doc)

            # Filtro per intervallo tra date (DATE_RANGE)
            elif date_value == "DATE_RANGE" and data.get("date_from_date") and data.get("date_to_date"):
                
                from_date_str = data.get("date_from_date")
                to_date_str = data.get("date_to_date")
                
                if from_date_str and to_date_str:
                    try:
                        # Parsing della data del documento e di quelle del range
                        doc_date = datetime.strptime(doc.get("date", ""), "%Y-%m")
                        from_date = datetime.strptime(from_date_str, "%Y-%m")
                        to_date = datetime.strptime(to_date_str, "%Y-%m")
                        
                        # Verifica se la data del documento si trova
                        # all'interno dell'intervallo specificato
                        if from_date <= doc_date <= to_date:
                            results.append(doc)
                    except Exception: pass

        # Restituzione
        return results

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        ##############################################################
        ## INIZIALIZZAZIONE PARAMETRI                               ##
        ##############################################################

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            MyPyLucene.create_indexes()
        
        # Inizializzazione di Lucene
        MyPyLucene.init_lucene_vm()
        
        # Apertura directory
        fsDir = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        # Apertura del reader
        reader = DirectoryReader.open(fsDir)
        
        # Apertura del searcher
        searcher = IndexSearcher(reader)
        
        # Creazione dell'analizzatore
        analyzer = StandardAnalyzer()

        ###############################################################
        ## QUERY PRINCIPALE - RICERCA SUL CONTENUTO DEL DOCUMENTO    ##
        ###############################################################

        # Creazione parser per ricerca nel campo "content"
        parser = QueryParser("content", analyzer)

        # Impostazione dell'operatore AND di default per il parser
        # parser.setDefaultOperator(QueryParser.Operator.AND)

        # Parsing della query principale sul campo
        content_query = parser.parse(data["ricerca_principale"])
        
        #######################################################################
        ## RICERCA SU PIU' CAMPI - CREAZIONE DI UNA QUERY BOOLEANA COMBINATA ##
        #######################################################################
        
        ## Enum BooleanClause.Occur.
        ## https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/BooleanClause.Occur.html
        # FILTER - Like MUST except that these clauses do not participate in scoring.
        # MUST - Use this operator for clauses that must appear in the matching documents.
        # MUST_NOT - Use this operator for clauses that must not appear in the matching documents.
        # SHOULD - Use this operator for clauses that should appear in the matching documents.

        # Termini di ricerca secondari
        run_terms_search = data["terms"]

        # Se ci sono termini da cercare
        if run_terms_search:
            
            # Inizializzazione di un costruttore per la query booleana
            terms_query_builder = BooleanQuery.Builder()

            # Itera attraverso ogni termine di ricerca
            for term_data in data["terms"]:
                
                # Recupero operatore e campo
                term = term_data["term"]
                operator = term_data["operator"].strip().upper()
                field = term_data["field"].strip().upper()

                # Mappatura tra operatori e clausole di Lucene
                operator_mapping = {
                    "AND": BooleanClause.Occur.MUST,
                    "NOT": BooleanClause.Occur.MUST_NOT,
                    "OR": BooleanClause.Occur.SHOULD
                }

                # Imposta l'operatore di ricerca
                op = operator_mapping.get(operator, BooleanClause.Occur.SHOULD)  # Default è SHOULD

                # Mappatura tra chiavi e nomi dei campi
                field_mapping = {
                    "TITLE": "title",           # Titolo
                    "DESCRIPTION": "abstract",  # Estratto
                    "KEYWORDS": "keywords"      # Parole chiave
                }

                # Imposta il campo di ricerca
                field = field_mapping.get(field, "abstract") # Default è "abstract"

                # Crea il parser per il campo specificato
                parser = QueryParser(field, analyzer)
                
                # Costruzione della query per il termine
                query = parser.parse(term)
                
                # Aggiungi la query con l'operatore specificato
                terms_query_builder.add(query, op)

            # Completamento costruzione query booleana
            terms_query = terms_query_builder.build()
        
        ###########################################################################
        ## RICERCA PER STATO - CREAZIONE DI UNA QUERY PER LO STATO DEI DOCUMENTI ##
        ###########################################################################

        # TermQuery - Una TermQuery è una query semplice e diretta in Lucene che cerca un termine esatto in un campo specifico.
        # QueryParser - Il QueryParser è uno strumento di Lucene che permette di analizzare una stringa di query scritta in linguaggio naturale o quasi, e convertirla in una query Lucene. È più potente e versatile, ma richiede una stringa di input come query.
        
        # Verifica se ci sono i parametri per la ricerca dello stato
        run_status_search = any(data[key] for key in [
            "standard_track", "best_current_practice", "informational", "experimental", "historic"
        ])

        # Se ci sono parametri di stato
        if run_status_search:
            
            # Inizializzazione di un costruttore per la query booleana
            status_query_builder = BooleanQuery.Builder()

            # Mappatura tra i parametri di stato e i valori di stato
            status_mapping = {
                "best_current_practice": "Best Current Practice",
                "informational": "Informational",
                "experimental": "Experimental",
                "historic": "Historic",
            }

            # Aggiungi lo stato specifico per "standard_track"
            if data["standard_track"]:
                
                # Estrai il valore specificato per "standard_track"
                value = data["standard_track_value"].strip().upper()
                
                # Mappatura dei valori dello "standard_track"
                standard_track_mapping = {
                    "PROPOSED_STANDARD": "Proposed Standard",
                    "DRAFT_STANDARD": "Draft Standard",
                    "INTERNET_STANDARD": "Internet Standard",
                }
                
                # Se il valore specificato esiste nella mappatura
                if value in standard_track_mapping:
                    # Aggiungi la query per lo stato
                    status_query_builder.add(
                        TermQuery(Term("status", standard_track_mapping[value])), 
                        BooleanClause.Occur.SHOULD
                    )

            # Aggiungi gli altri stati mappati 
            # (Best Current Practice, Informational, Experimental, Historic)
            for key, status in status_mapping.items():
                # Verifica che lo stato sia stato selezionato
                if data[key]:
                    # Aggiungi la query per lo stato
                    status_query_builder.add(
                        TermQuery(Term("status", status)),
                        BooleanClause.Occur.SHOULD
                    )
            
            # Completamento costruzione query booleana
            status_query = status_query_builder.build()
        
        ###########################################################################
        ## COSTRUZIONE DELLA QUERY FINALE - COMBINAZIONE DELLE QUERY INDIVIDUALI ##
        ###########################################################################

        # Crea il costruttore per la query booleana finale
        # che combina le query (content, terms, status)
        final_query_builder = BooleanQuery.Builder()

        # Aggiungi la query sul contenuto del documento, obbligatoria (MUST)
        final_query_builder.add(content_query, BooleanClause.Occur.MUST)

        # Se è stato richiesto un filtro sui termini, aggiungi la query, obbligatoria (MUST)
        if run_terms_search: final_query_builder.add(terms_query, BooleanClause.Occur.MUST)
        
        # Se è stato richiesto un filtro sullo stato, aggiungi la query, obbligatoria (MUST)
        if run_status_search: final_query_builder.add(status_query, BooleanClause.Occur.MUST)
        
        # Se è stato richiesto un filtro sulla data, aggiungi la query, obbligatoria (MUST)
        #if run_date_search: final_query_builder.add(date_query, BooleanClause.Occur.MUST)
        
        #######################################################################################
        ## ESTRAZIONE DEI RISULTATI - ESECUZIONE DELLA RICERCA E FORMATTAZIONE DEI RISULTATI ##
        #######################################################################################

        # Esegue la ricerca con la query finale costruita e limita il numero di risultati
        scoreDocs = searcher.search(final_query_builder.build(), data.get("size", 25)).scoreDocs

        # Converte i risultati in formato JSON
        results = MyPyLucene._results_to_json(searcher, scoreDocs)
        
        #############################################################
        ## FILTRAGGIO PER DATA --- IMPLEMENTATA IN POST-PROCESSING ##
        #############################################################

        # Filtra i risultati ottenuti per data
        results = MyPyLucene._filter_results_by_date(data, results)
        
        # ########################################################### #
        
        # Restituzione
        return results

    # ########################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPyLucene._execute_query(query)

# ########################################################### #

if __name__ == "__main__":
    
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

    #test_indexes_creation()
    #test_query_execution()