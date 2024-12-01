from project.searchengine.myLogger import logger as logging, bcolors

import os
import sys
import subprocess

def webserver():
    print(bcolors.GREEN + "Starting web server ..." + bcolors.RESET)
    subprocess.run("cd ")
    

def parser():
    print(bcolors.GREEN + "Starting parser ..." + bcolors.RESET)

def help():
    msg = """
+------------- Help Page --------------+
|  syntax: python graboid.py -[h,w,p]  |
|  -h Show Help                        |
|  -w Start web server                 |
|  -p Start parser                     |
+--------------- [1/1] ----------------+"""
    print(msg)
        
def error(flag) -> callable:
    logging.error(f"La flag '{flag}' non è supportata!")
    logging.info("Consulta la guida tramite il comando: \"python graboid.py -h\"")
    help()

EXPECTED_DIR = 'gestione-info'
CURRENT_DIR = os.path.basename(os.path.abspath(os.getcwd()))

STARTER = {
    "-w" : webserver,
    "-p" : parser,
    "-h" : help
}

if __name__ == '__main__':
    # Controllo che lo script venga effettuato nella directory giusta
    if CURRENT_DIR != EXPECTED_DIR:
        logging.critical(f'Esegui lo script stando nella directory indicata ({CURRENT_DIR}).')
        sys.exit(1)
    
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        STARTER.get(flag, lambda: error(flag))()
        sys.exit(0)