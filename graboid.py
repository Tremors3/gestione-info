from project.searchengine.myLogger.myLogger import logger as logging, bcolors
from sys import platform

import os
import sys
import subprocess

def install_dependencies():
    
    # Installazione delle dipendenze
    logging.debug(f"Scarico i requirements dal file {PathList.REQUIREMENTS_FILE}...")
    execute_subprocess([PathList.PYTHON_EXECUTABLE, "-m", "pip", "install", "--upgrade", "pip"])        
    execute_subprocess([PathList.PYTHON_EXECUTABLE, "-m", "pip", "install", "-r", PathList.REQUIREMENTS_FILE])
    
    logging.debug("Requirements scaricati con successo.")

def check_or_create_venv():
    """Funzione per controllare sia l'esistenza del virtual environment che del file requirements
       e della loro eventuale creazione/installazione dipendenze"""

    # Controllo di esistenza del venv
    if os.path.isfile(PathList.PYTHON_EXECUTABLE) and Options.SYNC_DEPS == False:
        logging.debug("Virtual environment rilevato.")
        return
    
    try:
        
        # Controllo sull'esistenza del file requirements
        if not os.path.isfile(PathList.REQUIREMENTS_FILE):
            logging.error(f"Il file \'{PathList.REQUIREMENTS_FILE}' non esiste. Non è possibile installare le dipendenze.")
            sys.exit(1)
        
        if not os.path.isfile(PathList.PYTHON_EXECUTABLE):
            
            # Creazione del virtual environment
            logging.debug("Creazione virtual environment ...")
            execute_subprocess(["python","-m","venv","venv"])
        
            # Controllo di esistenza del venv
            if not os.path.isfile(PathList.PYTHON_EXECUTABLE):
                logging.error("Non è stato possibile creare il virtual environment.")
                sys.exit(1)
            
            logging.debug("Virtual environment creato con successo.")
        
        # Installazione delle dipendenze
        install_dependencies()

    except Exception as e:
        logging.error(f"Errore durante la creazione del virtual environment: {e}")
        sys.exit(1)

# -------------------------------------- DA INTEGRARE --------------------------------------

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
    
    # Cerchiamo ed eventualmente creiamo il venv
    check_or_create_venv()
    
    # Controllo di esistenza del venv
    if not os.path.isfile(PathList.PYTHON_EXECUTABLE):
        logging.error(f"L'eseguibile Python non è stato trovato nel virtual environment: \'{PathList.PYTHON_EXECUTABLE}\'")
        return
    
    # Esecuzione degli scripts
    execute_subprocess([PathList.PYTHON_EXECUTABLE, script_path])
    
def webserver():
    """Avvio del webserver con la flag -w"""
    print(bcolors.GREEN + "Starting web server ..." + bcolors.RESET)
    directory   = os.path.join(PathList.WEB_APP_PATH)  # Webserver path
    script_path = os.path.join(directory, "run.py")  # Run Path
    process_starter(directory, script_path)  # Start Process

def parser():
    """Avvio del parser con la flag -p"""
    print(bcolors.GREEN + "Starting parser ..." + bcolors.RESET)
    directory   = os.path.join(PathList.SEARCH_ENGINE_PATH, "myParser")  # Parser path
    script_path = os.path.join(directory, "myParser.py")  # Run Path
    process_starter(directory, script_path)  # Start Process

def help():
    """Messaggio per la visualizzazione della pagina di help"""
    msg = """
+--------------- Help Page --------------------+
|  syntax:   python graboid.py -[h,w,p] [-s]  |
|
|  -h Show Help                             |
|  -w Start web server                      |
|  -p Start parser                          |
|  -s Sync dependencies                     |
+--------------- [1/1] ---------------------+"""
    print(msg)
    
def error(flag) -> callable:
    """Messaggio di errore nel caso venga inserita una flag sbagliata"""
    logging.error(f"La flag \'{flag}\' non è supportata.")
    logging.info("Consulta la guida tramite il comando: \'python graboid.py -h\'.")
    help()

class PathList:
    # Main Paths
    BASE_PATH    = "gestione-info"
    PROJECT_PATH = os.path.join("project")
    WEB_APP_PATH = os.path.join(PROJECT_PATH, "webapp")
    SEARCH_ENGINE_PATH = os.path.join(PROJECT_PATH, "searchengine")

    # VENV PATHS
    VENV_DIR     = BASE_PATH
    VENV_SUB_DIR = "Scripts" if platform == "win32" else "bin"
    PYTHON_EXTENSION  = ".exe" if platform == "win32" else ""
    PYTHON_EXECUTABLE = os.path.join("venv", VENV_SUB_DIR, f"python{PYTHON_EXTENSION}")

    # Other Paths
    CURRENT_DIR  = os.path.basename(os.path.abspath(os.getcwd()))
    EXPECTED_DIR = BASE_PATH

    # Requirements
    REQUIREMENTS_FILE = "requirements.txt"

class Options:
    SYNC_DEPS = False

    # Dizionario delle flag
    FUNCS = {
        "-w" : webserver,
        "-p" : parser,
        "-h" : help
    }

if __name__ == '__main__':

    # Controlliamo di aver eseguito lo script nella cartella giusta    
    if PathList.CURRENT_DIR != PathList.EXPECTED_DIR:
        logging.critical(f'Esegui lo script stando nella directory indicata: \'{PathList.EXPECTED_DIR}\'.')
        sys.exit(1)
    
    # Controllo ed esecuzione delle flag
    if len(sys.argv) > 1:
        
        if "-s" in sys.argv: 
            Options.SYNC_DEPS = True
            sys.argv.remove("-s")
        
        flag = sys.argv[1]
        Options.FUNCS.get(flag, lambda: error(flag))()