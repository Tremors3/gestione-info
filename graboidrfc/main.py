
# ################################################## #

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys, re, os

# ################################################## #

# Importazioni dei moduli del progetto
from graboidrfc.core.modules.docker.myDocker import DockerPG
from graboidrfc.core.modules.ui.run import start as start_web_server
from graboidrfc.core.modules.engines.myParser.myParser import start as start_parser
from graboidrfc.core.modules.engines.myBenchmark.createBenchmark import start as start_benchmark
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# Moduli dei tre motori di ricerca
from graboidrfc.core.modules.engines.myWhoosh.myWhoosh import MyWhoosh
from graboidrfc.core.modules.engines.myPostgres.myPostgres import MyPostgres
#from graboidrfc.core.modules.engines.myPylucene.myPylucene import MyPyLucene

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
        
        # INIZIALIZE ARGUMENT PARSER
        self.argparser = ArgumentParser(
            prog='graboidrfc',
            description='Script che inizializza e avvia l\'applicazione.',
            epilog='Esempio di utilizzo: graboidrfc --start',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        
        # Gruppo Auto-esclusivo
        exclusive_group = self.argparser.add_mutually_exclusive_group(required=True)
        
        # Argomenti Principali
        exclusive_group.add_argument('-i', '--init', action='store_true', help='Inizializza l\'applicazione.')
        exclusive_group.add_argument('-s', '--start', action='store_true', help='Avvia l\'applicazione.')
        exclusive_group.add_argument('-c', '--cleanup', action='store_true', help='Rimuove tutti i file creati durante la fase di inizializzazione.')
        
        # Docker Arguments
        exclusive_group.add_argument('-dc', '--docker-create', action='store_true', help='Crea e avvia il container docker di Postgres.')
        exclusive_group.add_argument('-dr', '--docker-remove', action='store_true', help='Rimuove il container docker di Postgres.')

    # #################################################################################################### #

    def dispatcher(self, method: str, *args) -> None:
        """Chiama la callback associata alla flag passata come argomento."""
        callback = getattr(self, method, None)
        if callback: callback(*args)
        return callback

    @staticmethod
    def _extract_methods(args, blacklist: list[str]) -> list[str]:
        """Funzione per preparare gli argomenti per il dispacher"""
        return [ f'{key}'.replace('-', '_').strip() for key, value in args.__dict__.items() if key.strip() not in blacklist and value ]

    def main(self):
        """ Entry point dell'applicazione """
        
        # Parsing degli argomenti
        parsed_args = self.argparser.parse_args()
        
        # Estrazione del nome del metodo da passare al dispacher
        method = __class__._extract_methods(parsed_args, blacklist=[]).pop()

        # Esecuzione del metodo associato all'argomento
        if not self.dispatcher(method):
            raise ValueError(f"Argomeno inserito non riconosciuto.")
    
    # ################################################## #

    # CALLBACKS

    def init(self) -> None:
        """Inizializza l'ambiente di produzione."""
        print(f"{bcolors.GREEN}Inizializzazione dell'applicazione...{bcolors.RESET}")

        self.docker_create() # Creazione container
        self.parser() # Costruzione del Dataset
        self.indexes() # Creazione degli Indici

    def start(self) -> None:
        """Avvia l'applicazione."""
        print(f"{bcolors.GREEN}Avvio dell'Applicazione...{bcolors.RESET}")
        
        self.web() # Procedura di avvio server web

    def cleanup(self) -> None:
        """Pulisce l'ambiente di sviluppo."""
        print(f"{bcolors.GREEN}Pulizia dell'ambiente di produzione completata.{bcolors.RESET}\n"
              f"È necessario inizializzare nuovamente per eseguire il programma.")
        
        self.docker_remove() # Cancellazione Container Docker
        
    # ################################################## #
    
    # OTHER METHODS
    
    def web(self) -> None:
        """Avvia il web server del progetto."""
        docker_pg = DockerPG()
        docker_pg.start()
        start_web_server() # Avvio Web Server
        docker_pg.stop()
    
    def parser(self) -> None:
        """Costruzione del dataset apportata dal parser."""
        print(f"{bcolors.GREEN}Costruzione del dataset...{bcolors.RESET}")
        start_parser() # Avvio Parser

    def indexes(self) -> None:
        """Costruisce gli Indici Invertiti."""
        print(f"{bcolors.GREEN}Costruzione degli Indici...{bcolors.RESET}")
        MyWhoosh.create_indexes() # Creazione indici Whoosh
        #MyPyLucene.create_indexes() # Creazione indici PyLucene
        docker_pg = DockerPG()
        docker_pg.start()
        postgres = MyPostgres()
        postgres.create_indexes() # Creazione indici Postgres
        del postgres
        docker_pg.stop()

    def docker_create(self) -> None:
        """Costruzione del container docker per postgres."""
        print(f"{bcolors.GREEN}Creazione container docker ...{bcolors.RESET}")
        DockerPG()

    def docker_remove(self) -> None:
        """Costruzione e rimozione del container docker."""
        print(f"{bcolors.GREEN}Cancellazione container docker ...{bcolors.RESET}")
        DockerPG().delete()

def main():
    app = Application()
    app.main()

if __name__ == "__main__":
    main()