from project.searchengine.myLogger import logger as logging, bcolors
from sys import platform

import os
import sys
import subprocess

def execute_subprocess(command: list):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Errore durante l'esecuzione del comando: {e}")
    except FileNotFoundError as e:
        logging.error(f"File o directory non trovati: {e}")
    except KeyboardInterrupt:
        logging.warning("Interruzione da tastiera.")

def process_starter(directory: str, script_path: str):
    
    # Controllo di esistenza della cartella
    if not os.path.isdir(directory):
        logging.error(f"La directory specificata \'{directory}\' non esiste. Verifica il percorso.")
        return

    # Controllo di esistenza del file 
    if not os.path.isfile(script_path):
        logging.error(f"Il file specificato \'{script_path}\' non esiste nella directory \'{directory}\'.")
        return
    
    # Deduzione della sottodirectory del venv data la piattaforma
    venv_path = "Scripts" if platform == "win32" else "bin"
    python_executable = os.path.join(directory, "venv", venv_path, "python")
    
    # Controllo di esistenza del file 
    if not os.path.isfile(python_executable):
        logging.error(f"L'eseguibile Python non è stato trovato nel virtual environment: \'{python_executable}\'")
        return
    
    # Esecuzione degli scripts
    execute_subprocess([python_executable, script_path])
    
def webserver():
    print(bcolors.GREEN + "Starting web server ..." + bcolors.RESET)
    
    directory = os.path.join("project", "webapp")  # Webserver path
    script_path = os.path.join(directory, "run.py")  # Run Path
    
    process_starter(directory, script_path)  # Start Process

def parser():
    print(bcolors.GREEN + "Starting parser ..." + bcolors.RESET)
    
    directory = os.path.join("workspace", "experiments")  # Parser path
    script_path = os.path.join(directory, "download-parsing", "parser.py")  # Run Path
    
    process_starter(directory, script_path)  # Start Process

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
    logging.error(f"La flag \'{flag}\' non è supportata.")
    logging.info("Consulta la guida tramite il comando: \'python graboid.py -h\'.")
    help()

EXPECTED_DIR = 'gestione-info'
CURRENT_DIR = os.path.basename(os.path.abspath(os.getcwd()))

STARTER = {
    "-w" : webserver,
    "-p" : parser,
    "-h" : help
}

if __name__ == '__main__':
    
    if CURRENT_DIR != EXPECTED_DIR:
        logging.critical(f'Esegui lo script stando nella directory indicata: \'{EXPECTED_DIR}\'.')
        sys.exit(1)
    
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        STARTER.get(flag, lambda: error(flag))()