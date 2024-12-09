import sys
from typing import Callable

# Disabilita la generazione dei file .pyc
sys.dont_write_bytecode = True

# Importazioni dei moduli del progetto
from project.webapp.run import start as start_web_server
from project.searchengine.myParser.myParser import start as start_parser
from project.searchengine.myBenchMark.createBenchMark import start as start_benchmark
from project.searchengine.myLogger.myLogger import bcolors, logging

# Importazione della funzione di aiuto
from graboid import help

def web_server() -> None:
    """Avvia il web server del progetto."""
    print(f"{bcolors.GREEN}Avvio del web server ...{bcolors.RESET}")
    start_web_server()

def parser() -> None:
    """Avvia il parser del motore di ricerca."""
    print(f"{bcolors.GREEN}Avvio del parser ...{bcolors.RESET}")
    #import time
    #start = time.time()
    start_parser()
    #end = time.time()
    #tot = str(end-start).split(".")
    #print("Tempo esecuzione:", tot[0] +"."+ tot[1][:4], "secondi")

def benchmark() -> None:
    """Avvia lo script che crea il benchmark."""
    print(f"{bcolors.GREEN}Creazione del Benchmark ...{bcolors.RESET}")
    start_benchmark()

def error(flag) -> callable:
    """Mostra un messaggio di errore per flag non supportate e suggerisce l'uso della guida"""
    logging.error(f"La flag \'{flag}\' non è supportata.")
    logging.info("Consulta la guida tramite il comando: \'python graboid.py -h\'.")
    help()

class Options:
    """Classe che contiene il dizionario delle opzioni disponibili"""
    # Dizionario delle flag
    FUNCS: dict[str, Callable[[], None]] = {
        "-w" : web_server,
        "-p" : parser,
        "-b" : benchmark
    }

if __name__ == "__main__":

    # Controllo degli argomenti passati da linea di comando
    if len(sys.argv) > 1 and len(sys.argv[1]):

        flag = sys.argv[1]

        # Esegui la funzione corrispondente o mostra un errore se la flag non è valida
        Options.FUNCS.get(flag, lambda: error(flag))()
    else:

        # Messaggio di default se non viene passata alcuna flag
        logging.info("Nessuna flag specificata. Usa \'python graboid.py -h\' per la guida.")
        help()
