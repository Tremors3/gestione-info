
# #################################################################################################### #

import re
import sys
import time
from typing import Callable, Any

# #################################################################################################### #

# Importazioni dei moduli del progetto
from graboidrfc.core.modules.docker.myDocker import DockerPG
from graboidrfc.core.modules.ui.run import start as start_web_server
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.engines.myParser.myParser import start as start_parser
from graboidrfc.core.modules.engines.myBenchmark.createBenchmark import start as start_benchmark

# #################################################################################################### #

from graboidrfc.core.modules.engines.myWhoosh.myWhoosh import MyWhoosh
from graboidrfc.core.modules.engines.myPostgres.myPostgres import MyPostgres
#from graboidrfc.core.modules.engines.myPylucene.myPylucene import MyPylucene

# #################################################################################################### #

# Disabilita la generazione dei file .pyc
sys.dont_write_bytecode = True

# #################################################################################################### #

def howMuchTimeDoesItTake(func: Callable) -> Callable:
    
    def wrapped(*args, **kwargs) -> Any:
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        tot = str(end-start).split(".")    
        print(f"L'esecuzione della funzione {func.__name__} ha impiegato:", tot[0] + "." + tot[1][:4], "secondi.")
        return value
    
    return wrapped

# #################################################################################################### #

class Application:
    
    def __init__(self):
        
        # Lista degli argomenti passati allo script
        self.args = sys.argv[1:]
    
    def dispatcher(self, flag: str, *args) -> None:
        """Chiama la callback associata alla flag passata come argomento."""
        method = re.sub(r"^--", "", flag).replace("-", "_").strip()
        callback = getattr(self, method, None)
        if callback: callback(*args)
        return callback
    
    def start(self):
        """ Entry point dell'applicazione """
        if len(self.args) and not self.dispatcher(self.args[0]):
            print(f"La flag '{self.args[0]}' non è supportata.")

    # #################################################################################################### #
    
    # INIZIALIZZAZIONE
    
    def init(self) -> None:
        """Inizializza l'ambiente di sviluppo."""
        print(f"{bcolors.GREEN}Inizializzazione dell'applicazione ...{bcolors.RESET}")

        # Costruzione del Dataset
        self.parser()

        # Creazione degli Indici
        self.indexes()

    # DOCKER

    def docker(self) -> None:
        """Costruzione ed avvio del container docker per postgres."""
        print(f"{bcolors.GREEN}Creazione container docker ...{bcolors.RESET}")
        DockerPG().start()

    def docker_remove(self) -> None:
        """Costruzione e rimozione del container docker per postgres."""
        print(f"{bcolors.GREEN}Cancellazione container docker ...{bcolors.RESET}")
        DockerPG().delete()

    # COMPONENTI

    @howMuchTimeDoesItTake
    def parser(self) -> None:
        """Costruzione del dataset apportata dal parser."""
        print(f"{bcolors.GREEN}Costruzione del dataset ...{bcolors.RESET}")
        start_parser()

    @howMuchTimeDoesItTake
    def indexes(self) -> None:
        """Costruisce gli Indici Invertiti."""
        print(f"{bcolors.GREEN}Costruzione degli Inverted Index ...{bcolors.RESET}")
        
        # Whoosh Indexes
        MyWhoosh.create_indexes()
        
        # PyLucene Indexes
        #MyPylucene.create_indexes()
        
        # Postgres Indexes
        docker_pg = DockerPG()
        docker_pg.start() # Apertura container
        postgres = MyPostgres()
        postgres.create_indexes()
        docker_pg.stop() # Chiusura container
    
    def web(self) -> None:
        """Avvia il web server del progetto."""
        print(f"{bcolors.GREEN}Avvio del web server ...{bcolors.RESET}")
        
        docker_pg = DockerPG()
        docker_pg.start() # Apertura container
        start_web_server()
        docker_pg.stop() # Chiusura container
    
    def benchmark(self) -> None:
        """Avvia lo script che crea il benchmark."""
        print(f"{bcolors.GREEN}Creazione del Benchmark ...{bcolors.RESET}")
        start_benchmark()

# #################################################################################################### #

if __name__ == "__main__":
    app = Application()
    app.start()