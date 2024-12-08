import os
import sys
import subprocess
from sys import platform

sys.dont_write_bytecode = True

from project.searchengine.myLogger.myLogger import logger as logging, bcolors

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
    if os.path.isfile(PathList.PYTHON_EXECUTABLE):
        logging.debug("Virtual environment rilevato.")
        if Options.SYNC_DEPS: install_dependencies()
        return
    
    try:
        
        # Controllo sull'esistenza del file requirements
        if not os.path.isfile(PathList.REQUIREMENTS_FILE):
            logging.error(f"Il file \'{PathList.REQUIREMENTS_FILE}' non esiste. Non è possibile installare le dipendenze.")
            sys.exit(1)

        # Creazione del virtual environment
        logging.debug("Creazione virtual environment ...")
        execute_subprocess([sys.executable,"-m","venv","venv"])
            
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
        subprocess.run(command, check=True, cwd=PathList.BASE_PATH)
    except subprocess.CalledProcessError as e:
        logging.error(f"Errore durante l'esecuzione del comando: {e}")
    except FileNotFoundError as e:
        logging.error(f"File o directory non trovati: {e}")
    except KeyboardInterrupt:
        logging.warning("Interruzione da tastiera.")

def process_starter(execute: list[str]):
    
    # Cerchiamo ed eventualmente creiamo il venv
    check_or_create_venv()
    
    # Esecuzione degli scripts
    execute_subprocess([PathList.PYTHON_EXECUTABLE, *execute])
    
def start(args: str):
    """Avvio dell'applicazione con l'opzione"""
    script_path = os.path.join("starter.py")  # Run Path
    process_starter(["-B", script_path, args])  # Start Process

class PathList:
    # Main Paths
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    # VENV PATHS
    VENV_SUB_DIR = "Scripts" if platform == "win32" else "bin"
    PYTHON_EXTENSION  = ".exe" if platform == "win32" else ""
    PYTHON_EXECUTABLE = os.path.join("venv", VENV_SUB_DIR, f"python{PYTHON_EXTENSION}")

    # Other Paths
    EXPECTED_DIR = "gestione-info"
    CURRENT_DIR  = os.path.basename(os.path.abspath(os.getcwd()))

    # Requirements
    REQUIREMENTS_FILE = "requirements.txt"

class Options:
    SYNC_DEPS = False

def help():
    """Messaggio per la visualizzazione della pagina di help"""
    msg = f"""
┌──────────────╢ Help Page ╟──────────────┐
│                                         │╲
│  SYNOPSIS                               │╲│
│       python graboid.py -[w,p,b,h] [-s] │╲│
│                                         │╲│
│  OPTIONS                                │╲│
│   -h  Show help                         │╲│
│   -w  Start web server                  │╲│
│   -p  Start parser                      │╲│
│   -b  Create benchmark                  │╲│
│   -s  Sync dependencies                 │╲│
│                                         │╲│
└─────────────────╢ 1/1 ╟─────────────────┘╲│ 
 ╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲│
  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"""
    print(msg)

if __name__ == '__main__':

    # Controlliamo di aver eseguito lo script nella cartella giusta    
    if PathList.CURRENT_DIR != PathList.EXPECTED_DIR:
        logging.critical(f'Esegui lo script stando nella directory indicata: \'{PathList.EXPECTED_DIR}\'.')
        sys.exit(1)
    
    # Controllo ed esecuzione delle flag
    if len(sys.argv) > 1:
        
        if "-s" in sys.argv: 
            sys.argv.remove("-s")
            Options.SYNC_DEPS = True
        
        if "-h" in sys.argv: 
            sys.argv.remove("-h")
            help()
            sys.exit(0)

        start(' '.join(sys.argv[1:]))