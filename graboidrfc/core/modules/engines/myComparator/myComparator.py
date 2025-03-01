
# Importazione standard
import os, json

# Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazione di moduli del progetto
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# ############################################################################ #

class MyComparator():

    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))

    # SETTINGS FILE PATHS
    SETTINGS_FILE_PATH = os.path.join(
        DYNAMIC_PACKAGE_PATH, "core", "config", "comparator.json"
    )

    # RESULTS FILE PATHS
    BENCHMARK_FOLDER = os.path.join(
        DYNAMIC_PACKAGE_PATH, "core", "data", "benchmark"
    )
    BENCHMARK_FILE_PATH = os.path.join(
        BENCHMARK_FOLDER, "benchmark.json"
    )
    LOCAL_RESULTS_FILE_PATH = os.path.join(
        BENCHMARK_FOLDER, "extracted_local.json"
    )
    
    # ################################################## #

    def __init__(self):
        self.initialize()
    
    # ################################################## #
    
    def initialize(self):
        
        self.settings = __class__.__load_json(
            self.SETTINGS_FILE_PATH
        )
        
        self.benchmark = __class__.__load_json(
            self.BENCHMARK_FILE_PATH
        )
        
        self.local_results = __class__.__load_json(
            self.LOCAL_RESULTS_FILE_PATH
        )
    
    @staticmethod
    def __load_json(file_path: str):
        """Funzione che legge e restutiusce un file in formato JSON."""
        
        # Controllo se il file esiste
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Il file non è stato trovato al seguente percorso: \'{file_path}\'.")

        try:
            
            # Lettura e restituzione contenuto in formato JSON
            with open(file_path, mode="r", encoding='utf-8') as f:
                return json.load(f)
            
        except Exception as e:
            raise Exception(f"Errore durante la lettura del file al seguente percorso \'{file_path}\': {e}")
    
    # ################################################## #
    
    def process(self):
        ...

    # ################################################## #

if __name__ == "__main__":
    comparator = MyComparator()
    comparator.process()