
# Altri import
import numpy as np, json, os

# Importazioni dei moduli del progetto
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

# ################################################## #

class SearchEngineResultsProcessor:
    """Classe per gestire e processare i risultati dai motori di ricerca."""

    def __init__(self, max_results=30, alpha=1):
        self.max_results = max_results
        self.alpha = alpha
        self.results_by_engine = []

    def add_search_engine_results(self, engine_name, results):
        """Aggiunge i risultati di un motore di ricerca."""
        
        processed_results = SearchEngineResultsProcessor.get_rfc_params(results[:self.max_results])
        
        self.results_by_engine.append({
            "motore": engine_name,
            "documents": processed_results
        })
    
    @staticmethod
    def get_rfc_params(results):
        """Estrae i numeri RFC dai risultati e tiene traccia della posizione migliore."""
        
        best_positions = {}
        
        position = 1
        for result in results:
            
            rfc_number = result if result.isdigit() else None
            
            if rfc_number and rfc_number not in best_positions:
                
                best_positions[rfc_number] = {"number": rfc_number, "position": position}
                position += 1
        
        return sorted(best_positions.values(), key=lambda x: x["position"])
    
    def clear_search_engine_results(self):
        """ Pulisce i risultati dei motori di ricerca """
        self.results_by_engine.clear()

    def aggregate_scores(self):
        """Aggrega i punteggi di rilevanza basati su posizione e frequenza."""
        
        aggregati = {}
        
        for engine in self.results_by_engine:
            for doc in engine["documents"]:
                
                doc_id = doc["number"]
                position = doc["position"]
                score = self._calculate_score(position)
                
                if doc_id not in aggregati:
                    aggregati[doc_id] = {"number": doc_id, "total_score": 0, "frequency": 0}
                    
                aggregati[doc_id]["total_score"] += score
                aggregati[doc_id]["frequency"] += 1
                
        return aggregati

    @staticmethod
    def _calculate_score(position):
        """Calcola il punteggio di rilevanza logaritmico basato sulla posizione."""
        
        return 1 / np.log2(position + 1)

    @staticmethod
    def normalize_relevance(scores):
        """Normalizza i punteggi tra 0.0 e 2.0."""
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [2.0] * len(scores)
        
        return [2 * (score - min_score) / (max_score - min_score) for score in scores]

    def calculate_final_relevance(self, aggregated_data):
        """Calcola i punteggi finali combinando posizione e frequenza."""
        
        documents = []
        
        for doc_id, values in aggregated_data.items():
            relevance = values["total_score"] * (1 + self.alpha * values["frequency"])
            documents.append({
                "number": doc_id,
                "relevance": relevance
            })
        
        if not documents:
            raise ValueError("Non ci sono documents per cui calcolare la rilevanza.")
        
        # TODO: Edit self.normalize_relevance(); modify doc['relevance'] directly instead of creating a separate relevance list.
        # Right now we are reassigning every relevance to the documents based on the position in the list; thas no good. 
        
        relevance = [doc["relevance"] for doc in documents]
        normalized = self.normalize_relevance(relevance)
        
        # TODO: edit also this because of the previous todo.
        
        for i, doc in enumerate(documents):
            doc["normalized"] = normalized[i] + 1
            doc["rounded"] = round(normalized[i]) + 1
        
        # Sorting
        documents = sorted(documents, key=lambda x: x['normalized'], reverse=True)
        
        return documents

# ################################################## #

class BenchmarkConstructor:
    
    # CURRENT & EXPECTED WORKING DIRECTORY PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY_PATH = os.path.abspath(os.getcwd())
    EXPECTED_WORKING_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))

    # SETTINGS & DIRECTORY PATHS
    SETTINGS_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "config", "benchmark.json")
    EXTRACTED_RESULTS_FILE = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "benchmark", "extracted_online_revisited.json")
    BENCHMARK_OUTPUT_FILE = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "benchmark", "benchmark.json")

    @staticmethod
    def start():
        """Funzione principale per eseguire il calcolo dei punteggi di rilevanza."""
        
        # Ottenimento delle impostazioni
        settings = BenchmarkConstructor.get_settings()
        
        # Configura il processore con i parametri desiderati
        processor = SearchEngineResultsProcessor(
            max_results=settings.get("MAX_RESULTS", 10), 
            alpha=settings.get("ALPHA", 1)
        )
        
        # Percorsi
        queries_file_name = BenchmarkConstructor.EXTRACTED_RESULTS_FILE
        result_file_name = BenchmarkConstructor.BENCHMARK_OUTPUT_FILE

        # Legge le query dal file JSON
        queries = BenchmarkConstructor.load_results_from_file(queries_file_name)
        if not queries:
            raise ValueError("Nessuna query trovata. Terminazione del programma.")
        
        # Processa le query e calcola i punteggi di rilevanza
        logging.debug('Costruzione del Benchmark...')
        benchmark = BenchmarkConstructor.process_queries(queries, processor)
        
        # Scrive i risultati sul file Json
        logging.info(f"Scrittura del Benchmark su File: '{result_file_name}'.")
        BenchmarkConstructor.save_results_to_file(benchmark, result_file_name)
        
        # Stampa i risultati
        BenchmarkConstructor.print_results(benchmark)
        
        # Ritorna il benchmark
        return benchmark

    @staticmethod
    def process_queries(queries, processor):
        """Elabora le query e calcola i punteggi di rilevanza."""
        benchmark = []
        
        for query in queries:
            query_text = query.get("query")
            results = query.get("results", {})
            
            # Processa i risultati per ciascun motore di ricerca
            for engine, urls in results.items():
                processor.add_search_engine_results(engine, urls) 
            
            # Aggrega e calcola i punteggi delle posizioni
            aggregated_data = processor.aggregate_scores()
            final_scores = processor.calculate_final_relevance(aggregated_data)
            
            # Pulisce i risultati associati alla query corrente
            processor.clear_search_engine_results()
            
            # Appende il risultato finale alla lista del benchmark 
            benchmark.append({"query": query_text, "relevance_values": final_scores})
        
        return benchmark

    @staticmethod
    def get_settings(fp:str=None):
        """Funzione che legge e restutiusce le impostazioni in formato JSON."""
        
        # Ottenimento del percorso del file delle impostazioni
        FILE_PATH = fp or __class__.SETTINGS_FILE_PATH
        
        # Controllo se il file delle impostazioni esiste
        if not os.path.isfile(FILE_PATH):
            raise FileNotFoundError(f"Il file delle configurazioni del banchmark non è stato trovato al seguente percorso: \'{FILE_PATH}\'.")

        # Lettura e restituzione delle impostazioni in formato JSON
        with open(FILE_PATH, mode="r", encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def print_results(benchmark):
        """Stampa i risultati calcolati."""
        
        print("Query e relativi documenti con rilevanza calcolata:")
        for query in benchmark:
            
            query_text = query.get("query")
            print(f"\nTesto della Query: '{query_text}'")
            
            for score in query.get("relevance_values", []):
                
                print(
                    f"Rfc: {score['number']}, ",
                    f"Rilevanza: {score['relevance']:.5f}, ",
                    f"Normalizzata: {score['normalized']:.5f}, ",
                    f"Arrotondata: {score['rounded']}"
                )
    
    @staticmethod
    def save_results_to_file(results: dict, filepath: str):
        """Salva i risultati in un file JSON nel directory temporaneo."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise IOError(f"Errore nel salvataggio del file {filepath}: {e}")

    @staticmethod
    def load_results_from_file(filepath: str):
        """Carica i risultati da un file JSON nel directory temporaneo."""
        try:
            if not os.path.isfile(filepath): return []
            with open(filepath, "r", encoding="utf-8") as f:
                return json.loads(f.read())
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Errore nella lettura del file {filepath}: {e}")
            return []

if __name__ == "__main__":
    BenchmarkConstructor.start()