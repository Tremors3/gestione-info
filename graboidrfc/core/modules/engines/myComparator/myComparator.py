
# Importazione standard
import os, json
from math import log2
from pprint import pprint
from functools import reduce
from typing import Dict, Tuple, List

# Importazione barra di caricamento
from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))

# Importazione di moduli del progetto
from graboidrfc.core.modules.utils.miscellaneous import safecast
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
    def calc_recall_precision(
        rel_docs: list[str], res_docs: list[str]) -> dict[float]:
        
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
                
                # Calcoliamo la recall e relativa precision, 
                # solamente se il documento è rilevante
                recall = __class__.calc_recall(rel_res_count, rel_docs_len)
                precision = __class__.calc_precision(rel_res_count, tot_res_count)
                
                results[recall] = precision

        return results

    @staticmethod
    def calc_interpolated_recall_precision(
        docs: dict, levels: int = 11, step: float = 0.1) -> dict:

        std_rec_lvls = {round(r * step, ndigits=1): 0 for r in range(0, levels)}
        
        for level in list(std_rec_lvls.keys())[::-1]:
            
            # Otteniamo i livelli di recall
            current_recall_level = level
            middle_recall_levels = (
                r for r in docs.keys()
                if current_recall_level < r < next_recall_level
            )
            next_recall_level = round(level + step, ndigits=1)
            
            # Otteniamo le precision associate
            current_precision = docs.get(current_recall_level, 0) # DOCS
            middle_precisions = [
                docs.get(r, 0)
                for r in middle_recall_levels
            ] # DOCS
            next_precision = std_rec_lvls.get(next_recall_level,0) # STD_REC_LVL
            
            # Uniamo le precisioni ottenute
            precisions = [current_precision] + middle_precisions + [next_precision]
            
            # Decretiamo quale sia la precision maggiore
            std_rec_lvls[level] = max(precisions)
        
        return std_rec_lvls

    # ################################################## #

    @staticmethod
    def calc_average(factors: list[float]) -> float:
        if not factors: return 0.0
        return sum(factors) / len(factors)

    # ################################################## #

    @staticmethod
    def calc_average_precision_at_recall(precision_per_query_at_r: list[float]) -> float:
        return MyComparator.calc_average(precision_per_query_at_r)
    
    @staticmethod
    def calc_all_average_precision_at_recall(precisions_per_query_per_r: dict[float, list[float]]) -> dict[float, float]:
        average_precision_per_recall_level = {}
        
        # Per ciascun livello di recall calcoliamo 
        # la media delle precisioni delle query
        for recall_level, precision_list in precisions_per_query_per_r.items():
            average_precision_per_recall_level[recall_level] = \
                MyComparator.calc_average_precision_at_recall(precision_list)
        
        return average_precision_per_recall_level

    @staticmethod
    def get_all_average_precision_at_recall(recalls_per_query: list[dict[float, float]]) -> dict[float, float]:
        data = {}

        # Per ciascun agglomerato di recall
        for recalls in recalls_per_query:
            
            # Per ciascun livello di recall e relativa precisione
            for recall_level, precision in recalls.items():
                
                # Se è la prima volta che incontriamo il livello di recall
                # allora inizializziamo il suo valore ad una lista vuota
                if not data.get(recall_level, None): data[recall_level] = []
                
                # Aggiunta della precision al livello
                data[recall_level].append(precision)

        return MyComparator.calc_all_average_precision_at_recall(data)

    # ################################################## #

    @staticmethod
    def calc_average_precision_of_query(precision_per_recall_of_q: list[float]) -> float:
        return MyComparator.calc_average(precision_per_recall_of_q)
    
    @staticmethod
    def calc_all_average_precision_of_query(queries: dict[str, list[float]]) -> dict[str, float]:
                
        average_precision_per_query = {}
        
        for query, precisions in queries.items():
            average_precision_per_query[query] = MyComparator.calc_average_precision_of_query(precisions)
    
        return average_precision_per_query
    
    @staticmethod
    def get_all_average_precision_of_query(queries: dict[str, dict[float, float]]) -> dict[str, float]:
                
        data = {}
        
        for query, recall_levels in queries.items():
            precisions = recall_levels.values()
            data[query] = precisions
        
        return MyComparator.calc_all_average_precision_of_query(data)

    # ################################################## #
    
    @staticmethod
    def calc_map(queries_average_precision: list[float]) -> float:
        return MyComparator.calc_average(queries_average_precision)
    
    @staticmethod
    def get_map(ap_per_query: dict[str, float]) -> float:
        return MyComparator.calc_map(ap_per_query.values())
    
    # ################################################## #
    
    @staticmethod
    def calc_harmonic_mean(sample: list[float]) -> float:
        
        if not sample or any((v == 0.0 for v in sample)):
            return 0.0
        
        return (len(sample) / sum(1 / v for v in sample))
    
    @staticmethod
    def calc_harmonic_mean_zero_adjusted(sample: list[float]) -> float:
        """https://search.r-project.org/CRAN/refmans/lmomco/html/harmonic.mean.html"""
        
        sample_size = len(sample)
        non_zero_values = [ v for v in sample if v != 0.0 ]
        non_zero_count = len(non_zero_values)
        
        if sample_size == 0 or non_zero_count == 0:
            return 0.0
        
        zero_value_correction = non_zero_count / sample_size
        non_zero_value_sum = sum(1 / v for v in non_zero_values)
        
        return (non_zero_count / non_zero_value_sum) * zero_value_correction
    
    @staticmethod
    def get_harmonic_mean(recall_precision: dict[float, float]) -> dict[float, float]:
        
        hm_fun = MyComparator.calc_harmonic_mean
        #hm_fun = MyComparator.calc_harmonic_mean_zero_adjusted
        
        f_measure_per_r = { r: hm_fun([r, v]) for r, v in recall_precision.items() }
        return f_measure_per_r

    # ################################################## #
    
    @staticmethod
    def extract_relevance(results_relevance: dict[str, int], results: list[str]) -> list[float]:
        return [ results_relevance.get(result, 0) for result in results ]
    
    @staticmethod
    def calc_discounted_cumulative_gain(relevance: list[float]) -> float:
        
        if not relevance: return 0.0

        dcg = relevance[0]
        dcg += sum(relevance[i] / log2(i + 1) for i in range(1, len(relevance)))
        
        return dcg
    
    @staticmethod
    def calc_normalized_discounted_cumulative_gain(ideal: list[float], relevance: list[float]) -> float:
        idcg = MyComparator.calc_discounted_cumulative_gain(sorted(ideal, reverse=True))
        dcg = MyComparator.calc_discounted_cumulative_gain(relevance)
        return dcg / idcg
    
    @staticmethod
    def get_normalized_discounted_cumulative_gain(results_relevance: dict[str, int], results: list[str]):
        return MyComparator.calc_normalized_discounted_cumulative_gain(
            ideal=results_relevance.values(),
            relevance=MyComparator.extract_relevance(results_relevance, results)
        )
    
    # ################################################## #

    def get_benchmark(benchmark: list) -> dict:
        """Mette i benchark in un dizionario più comodo da utilizzare"""
        res_benchmark = {}

        for i in benchmark:
            res_benchmark[i["num"]] = i
            
        return res_benchmark
    
    def calc_all_recall_precision_by_engine(self) -> dict:
        """Calcola recall e precision per engine"""

        benchmark_original = self.benchmark # Insieme degli R
        local_results = self.local_results # Insieme degli A
        benchmark = __class__.get_benchmark(benchmark=benchmark_original)
        
        RA = {}
        
        # Dizionari per ogni query
        for v in local_results.values():

            # Ogni engine utilizzato
            for engine in v["engines"].keys():
                RA[engine] = {}
                
                # Ogni funzione di ranking utilizzata
                for ranking in v["engines"][engine]:
                    RA[engine][ranking] = {}
                    res = {}

                    # Prende i risultati della query
                    for i, j in local_results.items():
                        # Calcola la recall e precision interpolata
                        res[i] = __class__.calc_interpolated_recall_precision(
                            __class__.calc_recall_precision(
                                [t["number"] for t in benchmark[int(i)]["relevance_values"]],
                                j["engines"][engine][ranking],
                            )
                        )

                        # Otteniamo la lista dei documenti rilevanti per la query
                        ideal_ordering_for_query = benchmark.get(safecast(i, int))
                        if ideal_ordering_for_query:
                            
                            # Otteniamo la lista delle rilevanze normalizzate per la query riferite ai documenti
                            ideal = { x["number"]: x["rounded"] for x in ideal_ordering_for_query["relevance_values"] }

                            if RA[engine][ranking].get("ndcg", None) is None:
                                RA[engine][ranking]["ndcg"] = {}
                            
                            # Calcolo della NDCG (Normalized Discounted Cumulative Gain)
                            RA[engine][ranking]["ndcg"][i] = \
                                __class__.get_normalized_discounted_cumulative_gain(
                                    results_relevance=ideal,
                                    results=local_results.get(safecast(i, str))["engines"][engine][ranking]
                                )
                    
                    # Calcola della precisione media (level) per engine
                    RA[engine][ranking]["avg_prec_at_std_rec_lvls"] = \
                        __class__.get_all_average_precision_at_recall(
                            res.values())
                    
                    # Calcolo della precisione media (query) per engine
                    RA[engine][ranking]["avg_prec_of_queries"] = \
                        __class__.get_all_average_precision_of_query(res)
                    
                    # Calcolo del valore MAP (Mean Average Precision) per engine
                    RA[engine][ranking]["map"] = __class__.get_map(
                        RA[engine][ranking]["avg_prec_of_queries"]
                    )

        return RA

    def calc_all_recall_precision_by_query(self) -> dict:
        """Calcola recall e precision per query"""
        
        benchmark = self.benchmark # Insieme degli R
        local_results = self.local_results # Insieme degli A
        
        RA = {}
        
        # Benchmark è una lista di dizionari        
        for element in benchmark:
            
            # Il numero della query
            query = safecast(element.get("num"), str)
            
            # Prendo i risultati per la query (Insieme A)
            result = local_results.get(query)
            
            # Prendo i risultati del benchmark (Insieme R)
            benchmark_numbers = [
                i.get("number") 
                for i in element.get("relevance_values")
            ]
            
            RA[query] = {}
            
            # Ogni engine utilizzato
            for se in result["engines"]:
                
                RA[query][se] = {}
                
                # Prende i modelli di ranking per il search engine
                ranking_models = result["engines"].get(se, [])
                
                # Ogni funzione di ranking utilizzata
                for rm in ranking_models:
                    
                    # Prende i risultati per la funzione di ranking per il 
                    # search engine
                    local_numbers = ranking_models.get(rm)

                    RA[query][se][rm] = {}
                    
                    # Ottengo recall e precision 
                    RA[query][se][rm]["recall_precision"] = \
                        __class__.calc_recall_precision(
                            benchmark_numbers,
                            local_numbers
                        )
                    
                    # Ottengo recall e precision interpolata
                    RA[query][se][rm]["recall_precision"] = \
                        __class__.calc_interpolated_recall_precision(
                            docs=RA[query][se][rm]["recall_precision"]
                        )
                    
                    # Ottengo la f-measure a ciascun livello standard di recall
                    RA[query][se][rm]["f_measure"] = \
                        __class__.get_harmonic_mean(
                            recall_precision=RA[query][se][rm]["recall_precision"]
                        )

        return RA

    # ################################################## #

if __name__ == "__main__":
    pass