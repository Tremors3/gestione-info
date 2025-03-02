
# Importazione standard
import os, json
from pprint import pprint
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
        
        # self.settings = __class__.__load_json(
        #     self.SETTINGS_FILE_PATH
        # )
        
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
    
    @staticmethod
    def calc_recall(rel_res: int, rel_tot: int) -> float:
        return float(rel_res / rel_tot)
    
    @staticmethod
    def calc_precision(rel_res: int, res_tot: int) -> float:
        return float(rel_res / res_tot)
    
    @staticmethod
    def calc_recall_precision(rel_docs: list[str], res_docs: list[str]):
        
        results = {}
        
        rel_docs_len = len(rel_docs) # Numero dei documenti rilevanti  |R|
        rel_res_count = 0 # Numero dei documenti restituiti rilevanti  |Ra|
        tot_res_count = 0 # Numero dei documenti restituiti            |A|
        
        for res_doc in res_docs:
            
            # Nuovo documento restituito
            tot_res_count += 1
            
            # Il nuovo documento restituito è anche rilevante?
            if res_doc in rel_docs:
                
                # Nuovo documento restituito rilevante
                rel_res_count += 1
                
                # Calcoliamo la recall e relativa precision, solamente se il documento è rilevante
                recall = __class__.calc_recall(rel_res_count, rel_docs_len)
                precision = __class__.calc_precision(rel_res_count, tot_res_count)
                
                results[recall] = precision

        return results

    @staticmethod
    def calc_interpolated_recall_precision(rel_docs: list[str], res_docs: list[str]):
        pass
        

    def all_recall(self):
        benchmark = self.benchmark # R
        local_results = self.local_results # A
        RA = {}

        # Benchmark è una lista di dizionari        
        for element in benchmark:

            # Prendo la query
            query = element.get("query").strip("site:www.rfc-editor.org").strip()
            
            # Prendo i risultati locali per la query (A)
            result = local_results.get(query)
            
            # Prendo i risultati del benchmark (R)
            benchmark_numbers = [i.get("number") for i in element.get("relevance_values")]
            
            RA[query] = {}

            for se in result:
                RA[query][se] = {}
                ranking_models = result.get(se)

                for rm in ranking_models:
                    local_numbers = ranking_models.get(rm)
                    RA[query][se][rm] = __class__.calc_recall_precision(
                        benchmark_numbers,
                        local_numbers
                    )

        pprint(RA)

    # ################################################## #
    
    def process(self):
        # self.all_recall()
        print(
            self.calc_recall_precision(rel_docs=["1","2","3","4"], res_docs=["1", "7", "3", "4", "5", "2"])
        )

        self.all_recall()

    # ################################################## #

if __name__ == "__main__":
    comparator = MyComparator()
    comparator.process()