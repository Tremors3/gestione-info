
# https://lucene.apache.org/core/10_0_0/

# #################################################################################################### #

import os, sys, json, shutil

# #################################################################################################### #

import lucene

from java.nio.file import Paths

from org.apache.lucene.util import Version

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import NIOFSDirectory

from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

# #################################################################################################### #

#from project.searchengine.myLogger.myLogger import logger as logging, bcolors

# #################################################################################################### #

class MyPyLucene:
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    INDEX_DIRECTORY_PATH = os.path.join(CURRENT_FILE_PATH, "indexes_dir")
    #DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")

    @staticmethod
    def _prepare_folders_and_files():
        """ Funzione che prepara la cartella degli indici. """
        
        # Controllo se il file del dataset esiste
        if not os.path.isfile(MyPyLucene.DATASET_FILE_PATH):
            #logging.error(f"Il file del dataset non è stato trovato al seguente percorso: \'{MyPyLucene.DATASET_FILE_PATH}\'.")
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
        
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        
        directory = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        analyzer = StandardAnalyzer()
        #analyzer = LimitTokenCountAnalyzer(analyzer, MyPyLucene.NoT)
        
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)
        
        # Apertura del file del dataset
        with open(MyPyLucene.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)
            print(f"Numero di documenti nel JSON: {len(documents)}")
        
        count=0
        for jdoc in documents:

            count += 1

            doc = Document()
        
            # Stored Fields
            doc.add(Field("number",     jdoc["Number"],              StringField.TYPE_STORED))
            doc.add(Field("files",      " ".join(jdoc["Files"]),     TextField.TYPE_STORED))
            doc.add(Field("title",      jdoc["Title"],               TextField.TYPE_STORED))
            doc.add(Field("authors",    " ".join(jdoc["Authors"]),   TextField.TYPE_STORED))
            doc.add(Field("date",       jdoc["Date"],                TextField.TYPE_STORED))
            doc.add(Field("more_info",  jdoc["More Info"],           StringField.TYPE_STORED))
            doc.add(Field("status",     jdoc["Status"],              StringField.TYPE_STORED))
            doc.add(Field("abstract",   jdoc["Abstract"],            TextField.TYPE_STORED))
            
            # Not Stored
            doc.add(Field("keywords",   " ".join(jdoc["Keywords"]),  TextField.TYPE_NOT_STORED))
            doc.add(Field("content",    jdoc["Content"],             TextField.TYPE_NOT_STORED))
            
            # Adding document to writer
            writer.addDocument(doc)

        print(f"Number of indexed documents: {count}")

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
        """Converte i risultati di Whoosh in un formato JSON-friendly."""
                
        results_list = []
        
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)  # Recupera il documento

            # Crea un dizionario con i campi memorizzati
            result = {}
            
            for field_name in ["title", "abstract", "content", "number", "files", "authors", "date"]:
                
                field_value = doc.get(field_name)
                
                if field_value:  # Se il campo esiste, aggiungilo al dizionario
                    result[field_name] = field_value

            results_list.append(result)
        
        return results_list  

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            MyPyLucene.create_indexes()
        
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        
        fsDir = NIOFSDirectory(Paths.get(MyPyLucene.INDEX_DIRECTORY_PATH))
        
        reader = DirectoryReader.open(fsDir)
        
        searcher = IndexSearcher(reader)
        
        analyzer = StandardAnalyzer()
        
        print(f"Numero di documenti nell'indice: {reader.numDocs()}")  # Mostra il numero di documenti
        
        parser = QueryParser("content", analyzer) # "keywords"
        
        parser.setDefaultOperator(QueryParser.Operator.AND)
        
        query = parser.parse(data["ricerca_principale"])
        
        scoreDocs = searcher.search(query, data.get("size")).scoreDocs
        
        results = MyPyLucene._results_to_json(searcher, scoreDocs)
        
        return results
    
    # #################################################################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPyLucene._execute_query(query)

# #################################################################################################### #

if __name__ == "__main__":
    
    #MyPyLucene.create_indexes()
    
    results = MyPyLucene._execute_query(data = {
        "ricerca_principale": "QUIC Protocol",
        "size": 5
    })
    
    for doc in results:
        print(doc, '\n')