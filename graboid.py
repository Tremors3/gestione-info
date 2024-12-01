from project.searchengine.myLogger import logger as logging, bcolors
from sys import platform

import os
import sys
import subprocess

# -------------------------------------- DA INTEGRARE --------------------------------------
def requirements():
    """Funzione per controllare l'esistenza del 
    file dei requirements e del loro eventuale download"""
    
    file = "requirements.txt"
    cartella = "project"
    if file in os.listdir(cartella):
        download_requirements = input(bcolors.WARNING+f"Scarico i requirements presenti in {file}? (Y/n)"+bcolors.RESET) or "Y"
        if download_requirements.lower() == "y":
            try:
                subprocess.run("")
                logging.info("Requirements scaricati con successo.")
                return True
            except Exception as e:
                logging.error(f"Errore durante il download dei requirements: {e}")
                return False
        else:
            return False
    else:
        logging.critical(f"Non ho trovato il file {file} per scaricare i requirements.\nControlla che sia nella cartella {cartella} e che abbia il nome giusto.")

def check_for_venv():
    """Funzione per controllare l'esistenza del 
       virtual environment e della sua eventuale 
       creazione"""
    
    venv = "venv"
    cartella = "project"
    # Cerco il virtual enviroment nella cartella del progetto
    if venv in os.listdir(cartella): 
        return True
    else:
        # Prompt per l'user
        create_venv = input(bcolors.WARNING+f"Non è stato rilevato nessun virtual environment ({venv}). Vuoi crearne uno adesso? (Y/n)"+bcolors.RESET) or "Y"
        
        if create_venv.lower() == "y":
            try:
                # Creazione del virtual environment
                subprocess.run(f"cd {cartella} & python -m venv {venv}")
                logging.info("Virtual environment creato con successo")
                return True
            
            except Exception as e:
                logging.error(f"Errore durante la creazione del virtual environment: {e}")
                return False
            
        else:
            return False
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
    
    # Deduzione della sottodirectory del venv data la piattaforma
    venv_path = "Scripts" if platform == "win32" else "bin"
    python_executable = os.path.join(directory, "venv", venv_path, "python")
    
    # Controllo di esistenza del venv
    if not os.path.isfile(python_executable):
        logging.error(f"L'eseguibile Python non è stato trovato nel virtual environment: \'{python_executable}\'")
        return
    
    # Esecuzione degli scripts
    execute_subprocess([python_executable, script_path])
    
def webserver():
    """Avvio del webserver con la flag -w"""
    print(bcolors.GREEN + "Starting web server ..." + bcolors.RESET)
    directory = os.path.join("project", "webapp")  # Webserver path
    script_path = os.path.join(directory, "run.py")  # Run Path
    process_starter(directory, script_path)  # Start Process

def parser():
    """Avvio del parser con la flag -p"""
    print(bcolors.GREEN + "Starting parser ..." + bcolors.RESET)
    directory = os.path.join("workspace", "experiments")  # Parser path
    script_path = os.path.join(directory, "download-parsing", "parser.py")  # Run Path
    process_starter(directory, script_path)  # Start Process

def help():
    """Messaggio per la visualizzazione della pagina di help"""
    msg = """
+------------- Help Page --------------+
|  syntax: python graboid.py -[h,w,p]  |
|  -h Show Help                        |
|  -w Start web server                 |
|  -p Start parser                     |
+--------------- [1/1] ----------------+"""
    print(msg)
        
def error(flag) -> callable:
    """Messaggio di errore nel caso venga inserita una flag sbagliata"""
    logging.error(f"La flag \'{flag}\' non è supportata.")
    logging.info("Consulta la guida tramite il comando: \'python graboid.py -h\'.")
    help()

EXPECTED_DIR = 'gestione-info'
CURRENT_DIR = os.path.basename(os.path.abspath(os.getcwd()))

# Dizionario delle flag
STARTER = {
    "-w" : webserver,
    "-p" : parser,
    "-h" : help
}

if __name__ == '__main__':

    # Controlliamo di aver eseguito lo script nella cartella giusta    
    if CURRENT_DIR != EXPECTED_DIR:
        logging.critical(f'Esegui lo script stando nella directory indicata: \'{EXPECTED_DIR}\'.')
        sys.exit(1)
    
    # Controllo ed esecuzione delle flag
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        STARTER.get(flag, lambda: error(flag))()