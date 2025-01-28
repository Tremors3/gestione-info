
# #################################################################################################### #

import os
import sys
import subprocess

from pathlib import Path
from sys import platform
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# #################################################################################################### #

from project.searchengine.myLogger.myLogger import logger as logging, bcolors

# #################################################################################################### #

# Disabilita la generazione dei file .pyc
sys.dont_write_bytecode = True

# #################################################################################################### #

class Graboid:
    
    def __init__(self):
        self.initialize_paths()
        self.initialize_argparser()
    
    def initialize_paths(self):
        
        # CURRENT WORKING PATHS & FILES
        self.CURRENT_WORKING_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CURRENT_WORKING_DIRECTORY = os.path.basename(os.path.abspath(os.getcwd()))
        self.EXPECTED_WORKING_DIRECTORY = "gestione-info"

        # VIRTUAL ENVIROMENTS PATHS & FILES
        self.PYTHON_REQUIREMENTS_FILE = "requirements.txt"
        PYTHON_EXECUTABLE_EXTENSION = ".exe" if platform == "win32" else ""
        PYTHON_EXECUTABLE_FILE = f"python{PYTHON_EXECUTABLE_EXTENSION}"
        PYTHON_VENV_SUBDIRECTORY = "Scripts" if platform == "win32" else "bin"
        self.PYTHON_EXECUTABLE_FILE_PATH = str("venv" / Path(PYTHON_VENV_SUBDIRECTORY) / Path(PYTHON_EXECUTABLE_FILE))
        
        # APPLICATION SCRIPT FILE
        self.APPLICATION_SCRIPT_FILE_PATH = "starter.py"
    
    def initialize_argparser(self):
        
        # DEFAULT OPTIONS
        self.fsync = False
        
        # INIZIALIZE ARGUMENT PARSER
        self.parser = ArgumentParser(
            prog='graboid',
            description='''
            Script che si occupa di inizializzare il Python Virtual Enviroment, 
            scaricare le appropriate dipendenze, ed eseguire le funzionalità 
            dell'applicazione al suo interno in modo da non sporcare l'ambiente 
            di sistema.''',
            epilog='''Esempio di utilizzo: python graboid.py -w -s''',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        
        # CURRENT SCRIPT ARGUMENTS
        self.excluded_arguments = ['sync']
        self.parser.add_argument('-s', '--sync', action='store_true', help='Forza la sincronizzazione delle dipendenze.')
        
        # APPLICATION SCRIPT ARGUMENTS
        exclusive_group = self.parser.add_mutually_exclusive_group(required=True)
        exclusive_group.add_argument('-i', '--init', action='store_true', help='Inizializza l\'applicazione.')
        exclusive_group.add_argument('-p', '--parser', action='store_true', help='Esegue il parser.')
        exclusive_group.add_argument('-w', '--web', action='store_true', help='Avvia il web server.')
        exclusive_group.add_argument('-b', '--benchmark', action='store_true', help='Crea i benchmark.')
        exclusive_group.add_argument('-x', '--indexes', action='store_true', help='Costruisce gli Inverted Index.')

    # #################################################################################################### #

    @staticmethod
    def _execute_subprocess(command: list[str], cwd: Path):
        try:
            subprocess.run(command, check=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            logging.error(f"Errore durante l'esecuzione del comando: {e}")
        except FileNotFoundError as e:
            logging.error(f"File o directory non trovati: {e}")
        except KeyboardInterrupt:
            logging.warning("Interruzione da tastiera.")

    def _install_dependencies(self):
        
        # Controllo sull'esistenza del file requirements
        if not os.path.isfile(self.PYTHON_REQUIREMENTS_FILE):
            logging.error(f"Il file \'{self.PYTHON_REQUIREMENTS_FILE}' non esiste. Non è possibile installare le dipendenze.")
            sys.exit(1)
        
        # Installazione delle dipendenze
        logging.debug(f"Scarico i requirements dal file {self.PYTHON_REQUIREMENTS_FILE}...")
        __class__._execute_subprocess([self.PYTHON_EXECUTABLE_FILE_PATH, "-m", "pip", "install", "--upgrade", "pip"], cwd=self.CURRENT_WORKING_DIRECTORY_PATH)
        __class__._execute_subprocess([self.PYTHON_EXECUTABLE_FILE_PATH, "-m", "pip", "install", "-r", self.PYTHON_REQUIREMENTS_FILE], cwd=self.CURRENT_WORKING_DIRECTORY_PATH)
        logging.debug("Requirements scaricati con successo.")

    def _check_or_create_venv(self):
        """Funzione per controllare sia l'esistenza del virtual environment sia la presenza del file requirements e della eventuale creazione/installazione delle relative dipendenze"""

        # Controllo di esistenza del venv
        if os.path.isfile(self.PYTHON_EXECUTABLE_FILE_PATH):
            logging.debug("Virtual environment rilevato.")
            if self.fsync: self._install_dependencies()
            return
        
        try:

            # Creazione del virtual environment
            logging.debug("Creazione virtual environment ...")
            __class__._execute_subprocess([sys.executable, '-m', 'venv', 'venv'], cwd=self.CURRENT_WORKING_DIRECTORY_PATH)
            
            # Controllo di esistenza del venv
            if not os.path.isfile(self.PYTHON_EXECUTABLE_FILE_PATH):
                logging.error("Non è stato possibile creare il virtual environment.")
                sys.exit(1)
            
            logging.debug("Virtual environment creato con successo.")
            
            # Installazione delle dipendenze
            self._install_dependencies()

        except Exception as e:
            logging.error(f"Errore durante la creazione del virtual environment: {e}")
            sys.exit(1)

    def _process_starter(self, arguments: list[str]):
        """Funzione per eseguire lo script di avvio dell'applicazione"""
        
        # Cerchiamo ed eventualmente creiamo il venv
        self._check_or_create_venv()
        
        # Esecuzione dello script
        try:
            __class__._execute_subprocess([self.PYTHON_EXECUTABLE_FILE_PATH, *arguments], cwd=self.CURRENT_WORKING_DIRECTORY_PATH)
        except Exception as e:
            if (e.code == 100): self.parser.print_help()
            else: logging.error(f"Errore durante l'esecuzione dello script: {e}")
                
    @staticmethod
    def _prepare_arguments(args, blacklist: list[str]):
        """Funzione per preparare gli argomenti da passare allo script"""
        return [ f'--{key.replace("_", "-")}' for key, value in args.__dict__.items() if key not in blacklist and value ]
    
    def start(self):
        """Entry Point dello Script"""
        
        # Parsing degli argomenti
        parsed_args = self.parser.parse_args()
        
        # Salvataggio dell'opzione sync
        self.fsync = parsed_args.sync
        
        # Preparazione degli argomenti da passare allo script
        script_args = __class__._prepare_arguments(parsed_args, blacklist=self.excluded_arguments)

        # Esecuzione dello script di avvio dell'applicazione
        self._process_starter([
            '-B', self.APPLICATION_SCRIPT_FILE_PATH, *script_args
        ]) # Start Process

# #################################################################################################### #

if __name__ == '__main__':
    graboid = Graboid()
    graboid.start()