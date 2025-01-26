
# https://lucene.apache.org/core/10_0_0/

# #################################################################################################### #

import os, sys, json, shutil

# #################################################################################################### #

import lucene
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField, DateField, KeywordField
from org.apache.lucene.store import NIOFSDirectory

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
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "example.json")
    
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
        
        directory = NIOFSDirectory(Paths.get(sys.argv[1]))
        
        analyzer = StandardAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)
        
        # Apertura del file del dataset
        with open(MyWhoosh.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)
        
        for jdoc in documents:
            
            doc = Document()
        
            # Stored Fields
            doc.add(Field("number",     jdoc["Number"],              StringField.TYPE_STORED))
            doc.add(Field("files",      " ".join(jdoc["Files"]),     TextField.TYPE_STORED))
            doc.add(Field("title",      jdoc["Title"],               TextField.TYPE_STORED))
            doc.add(Field("authors",    " ".join(jdoc["Authors"]),   TextField.TYPE_STORED))
            doc.add(Field("date",       jdoc["Date"],                DateField.TYPE_STORED))
            doc.add(Field("more_info",  jdoc["More Info"],           StringField.TYPE_STORED))
            doc.add(Field("status",     jdoc["Status"],              StringField.TYPE_STORED))
            doc.add(Field("abstract",   jdoc["Abstract"],            TextField.TYPE_STORED))
            
            # Not Stored
            doc.add(Field("keywords",   " ".join(jdoc["Keywords"]),  KeywordField.TYPE_NOT_STORED))
            doc.add(Field("content",    jdoc["Content"],             TextField.TYPE_NOT_STORED))
            
            # Adding document to writer
            writer.addDocument(doc)

        writer.commit()
        writer.close()

    @staticmethod
    def create_indexes():
        """ Funzione che crea gli indici per la ricerca. """
        MyPyLucene._prepare_folders_and_files()
        MyPyLucene._write_indexes()

    # #################################################################################################### #
        
    @staticmethod
    def _results_to_json(results):
        """Converte i risultati di Whoosh in un formato JSON-friendly."""
        pass

    @staticmethod
    def _execute_query(data: dict):
        """ Funzione che esegue la query di ricerca. """

        # Controllare se è necessario indicizzare i documenti
        if not os.path.exists(MyPyLucene.INDEX_DIRECTORY_PATH):
            MyPyLucene.create_indexes()
        
        results = ""
            
        return results
    
    # #################################################################################################### #
    
    @staticmethod
    def process(query: dict):
        return MyPyLucene._execute_query(query)

# #################################################################################################### #

if __name__ == "__main__":
    MyPyLucene.create_indexes()