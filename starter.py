
# #################################################################################################### #

import sys
import time
from typing import Callable, Any

# #################################################################################################### #

# Importazioni dei moduli del progetto
from project.webapp.run import start as start_web_server
from project.searchengine.myParser.myParser import start as start_parser
from project.searchengine.myBenchmark.createBenchMark import start as start_benchmark
from project.searchengine.myLogger.myLogger import bcolors, logging

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
        method = flag.replace("--", "").strip()
        callback = getattr(self, method, None)
        if callback: callback(*args)
        return callback
    
    def start(self):
        """ Entry point dell'applicazione """
        if len(self.args) and not self.dispatcher(self.args[0]):
            logging.error(f"La flag '{self.args[0]}' non è supportata.")

    # #################################################################################################### #
    
    def init(self) -> None:
        """Inizializza l'ambiente di sviluppo."""
        print(f"{bcolors.GREEN}Inizializzazione dell'applicazione ...{bcolors.RESET}")
        
        # Costruzione del Dataset
        self.parser()
        
        # Creazione degli Indici
        self.indexes()

    @howMuchTimeDoesItTake
    def parser(self) -> None:
        """Costruzione del dataset apportata dal parser."""
        print(f"{bcolors.GREEN}Costruzione del dataset ...{bcolors.RESET}")
        start_parser()

    @howMuchTimeDoesItTake
    def indexes(self) -> None:
        """Costruisce gli Indici Invertiti."""
        print(f"{bcolors.GREEN}Costruzione degli Indici Invertiti ...{bcolors.RESET}")
        pass
    
    def web(self) -> None:
        """Avvia il web server del progetto."""
        print(f"{bcolors.GREEN}Avvio del web server ...{bcolors.RESET}")
        start_web_server()
        
    def benchmark(self) -> None:
        """Avvia lo script che crea il benchmark."""
        print(f"{bcolors.GREEN}Creazione del Benchmark ...{bcolors.RESET}")
        start_benchmark()

# #################################################################################################### #

if __name__ == "__main__":
    app = Application()
    app.start()