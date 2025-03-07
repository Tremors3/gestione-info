
# ################################################## #

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys, re, os

# ################################################## #

# Importazioni dei moduli del progetto
from graboidrfc.core.modules.docker.myDocker import DockerPG
from graboidrfc.core.modules.web.run import start as start_web_server
from graboidrfc.core.modules.engines.myParser.myParser import start as start_parser
from graboidrfc.core.modules.engines.myBenchmark.benchmark import BenchmarkConstructor
from graboidrfc.core.modules.engines.myBenchmark.extractor_online import ExtractorOnline
from graboidrfc.core.modules.engines.myBenchmark.extractor_local import ExtractorLocal
from graboidrfc.core.modules.engines.myComparator.myGraphs import MyGraphs
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# Moduli dei tre motori di ricerca
from graboidrfc.core.modules.engines.myWhoosh.myWhoosh import MyWhoosh
from graboidrfc.core.modules.engines.myPostgres.myPostgres import MyPostgres
from graboidrfc.core.modules.engines.myPylucene.myPylucene import MyPyLucene

# ################################################## #

class Application:
    
    def __init__(self):
        self.initialize_paths()
        self.initialize_argparser()
    
    def initialize_paths(self):
        # CURRENT & EXPECTED WORKING DIRECTORY PATHS
        self.DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
        self.CURRENT_WORKING_DIRECTORY_PATH = os.path.abspath(os.getcwd())
        self.EXPECTED_WORKING_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
        
    def initialize_argparser(self):
        
        # Variabili Utili
        self.dockerpg = None
        self.use_docker = False
        
        # INIZIALIZE ARGUMENT PARSER
        self.argparser = ArgumentParser(
            prog='graboidrfc',
            description='Script che inizializza e avvia l\'applicazione.',
            epilog='Esempio di utilizzo: graboidrfc --start',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        
        # Utilizza Container Docker
        self.argparser.add_argument('-d', '--docker', action='store_true', help='Abilita l\'utilizzo del container docker per postgresql.')
        
        # Gruppo Auto-esclusivo
        exclusive_group = self.argparser.add_mutually_exclusive_group(required=True)
        
        # Argomenti Principali
        exclusive_group.add_argument('-i', '--init', action='store_true', help='Inizializza l\'applicazione.')
        exclusive_group.add_argument('-s', '--start', action='store_true', help='Avvia l\'applicazione.')
        # exclusive_group.add_argument('-c', '--cleanup', action='store_true', help='Rimuove tutti i file creati durante la fase di inizializzazione.')
        
        # Argomenti utili per Debugging
        exclusive_group.add_argument('-p', '--parser', action='store_true', help='Scarica e parserizza il dataset.')
        exclusive_group.add_argument('-x', '--indexes', action='store_true', help='Costruisce gli Inverted Index.')
        
        # Argomenti per la costruzione del Benchmark
        exclusive_group.add_argument('-e', '--extractor', action='store_true', help='Ottiene i risultati necessari alla costruzione del benchmark.')
        exclusive_group.add_argument('-l', '--extractor-local', action='store_true', help='Ottiene i risultati dei nostri tre search engine.')
        exclusive_group.add_argument('-b', '--benchmark', action='store_true', help='Costruisce e salva il benchmark.')

        # Argomenti per la costruzione dei grafici
        exclusive_group.add_argument('-g', '--graphs', action='store_true', help='Costruisce e salva i grafici.')        

    # #################################################################################################### #

    def dispatcher(self, method: str, *args) -> None:
        """Chiama la callback associata alla flag passata come argomento."""
        callback = getattr(self, method, None)
        if callback: callback(*args)
        return callback

    @staticmethod
    def _extract_methods(args, blacklist: set[str]) -> set[str]:
        """Funzione per preparare gli argomenti per il dispatcher"""
        return set( f'{key}'.replace('-', '_').strip() for key, value in args.__dict__.items() if key.strip() not in blacklist and value )

    def main(self):
        """ Entry point dell'applicazione """
        
        # Parsing degli argomenti
        parsed_args = self.argparser.parse_args()
        
        # Estrazione del nome del metodo da passare al dispatcher
        methods = __class__._extract_methods(parsed_args, blacklist=set())

        # Controllo se si vuole utilizzare Docker
        self.use_docker = 'docker' in methods
        methods.discard('docker')
        
        # Esecuzione del metodo associato all'argomento
        if methods and not self.dispatcher(methods.pop()):
            raise ValueError(f"Argomeno inserito non riconosciuto.")
    
    # ################################################## #

    # CALLBACKS METHODS

    def init(self) -> None:
        """Inizializza l'ambiente di produzione."""
        print(f"{bcolors.GREEN}Inizializzazione dell'applicazione...{bcolors.RESET}")
        
        self.parser() # Costruzione del Dataset
        self.indexes() # Creazione degli Indici

    def start(self) -> None:
        """Avvia l'applicazione."""
        print(f"{bcolors.GREEN}Avvio dell'Applicazione...{bcolors.RESET}")
        
        self.docker_start()
        self.web() # Procedura di avvio server web
        self.docker_stop()

    def cleanup(self) -> None:
        """Pulisce l'ambiente di sviluppo."""
        print(f"{bcolors.GREEN}Pulizia dell'ambiente di produzione completata.{bcolors.RESET}\n"
              f"È necessario inizializzare nuovamente per eseguire il programma.")
        
        # Cancellazione Container Docker
        self.docker_remove()
        
    # ################################################## #
    
    # OTHER METHODS
    
    def web(self) -> None:
        """Avvia il web server del progetto."""
        print(f"{bcolors.GREEN}Avvio del Server Web ...{bcolors.RESET}")
        start_web_server(use_docker=self.use_docker) # Avvio Web Server
    
    def parser(self) -> None:
        """Costruzione del dataset apportata dal parser."""
        print(f"{bcolors.GREEN}Costruzione del dataset ...{bcolors.RESET}")
        start_parser() # Avvio Parser

    def indexes(self) -> None:
        """Costruisce gli Indici Invertiti."""
        print(f"{bcolors.GREEN}Costruzione degli Indici ...{bcolors.RESET}")
        
        self.docker_start()
        postgres = MyPostgres(use_docker=self.use_docker)
        
        postgres.create_indexes() # Creazione indici Postgres
        
        postgres._close_connection()
        self.docker_stop()
        
        MyPyLucene.create_indexes() # Creazione indici PyLucene
        
        MyWhoosh.create_indexes() # Creazione indici Whoosh

    def extractor_local(self) -> None:
        """Avvia lo script per scaricare i risultati dei nostri search engine e li scrive su file"""
        print(f"{bcolors.GREEN}Estrazione dei risultati di PostgreSQL, PyLucene e Whoosh ...{bcolors.RESET}")
        ExtractorLocal.start()
    
    def extractor(self) -> None:
        """Avvia lo script che ottiene i risultati necessari alla costruzione del banchamrk."""
        print(f"{bcolors.GREEN}Estrazione dei risultati necessari alla costruzione del Banchmark ...{bcolors.RESET}")
        ExtractorOnline.start()

    def benchmark(self) -> None:
        """Avvia lo script calcola e mostra il benchmark."""
        print(f"{bcolors.GREEN}Costruzione e restituzione del Benchmark ...{bcolors.RESET}")
        BenchmarkConstructor.start()
    
    def graphs(self) -> None:
        """Avvia lo script che costruisce i grafici"""
        print(f"{bcolors.GREEN}Lettura risultati e costruzione grafici ...{bcolors.RESET}")
        MyGraphs.start()
    
    # ################################################## #

    def docker_start(self) -> None:
        """Costruzione e Avvio del container docker per postgres."""
        if self.use_docker and not self.dockerpg:
            print(f"{bcolors.GREEN}Creazione e Avvio container docker ...{bcolors.RESET}")
            self.dockerpg = DockerPG()
            self.dockerpg.start()

    def docker_stop(self) -> None:
        """Spegnimento del container docker."""
        if self.use_docker and self.dockerpg:
            print(f"{bcolors.GREEN}Spegnimento container docker ...{bcolors.RESET}")
            self.dockerpg.stop()
            self.dockerpg = None

    def docker_remove(self) -> None:
        """Rimozione del container docker."""
        if self.use_docker and self.dockerpg:
            print(f"{bcolors.GREEN}Rimozione container docker ...{bcolors.RESET}")
            self.dockerpg.delete()
            self.dockerpg = None

def main():
    app = Application()
    app.main()

if __name__ == "__main__":
    main()