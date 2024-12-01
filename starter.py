import sys

sys.dont_write_bytecode = True

from project.webapp.run import start as start_web_server
from project.searchengine.myParser.myParser import start as start_parser
from project.searchengine.myLogger.myLogger import bcolors, logging

from graboid import help

def web_server():
    print(bcolors.GREEN + "Avvio del web server ..." + bcolors.RESET)
    start_web_server()

def parser():
    print(bcolors.GREEN + "Avvio del parser ..." + bcolors.RESET)
    #import time
    #start = time.time()
    start_parser()
    #end = time.time()
    #tot = str(end-start).split(".")
    #print("Tempo esecuzione:", tot[0] +"."+ tot[1][:4], "secondi")

def error(flag) -> callable:
    """Messaggio di errore nel caso venga inserita una flag sbagliata"""
    logging.error(f"La flag \'{flag}\' non è supportata.")
    logging.info("Consulta la guida tramite il comando: \'python graboid.py -h\'.")
    help()
    
class Options:
    # Dizionario delle flag
    FUNCS = {
        "-w" : web_server,
        "-p" : parser,
        "-h" : help
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        Options.FUNCS.get(flag, lambda: error(flag))()