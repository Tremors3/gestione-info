import os
import json
import random
import numpy as np

class RFCReader:
    """Classe per il recupero degli URL risultanti delle query."""
    
    @staticmethod
    def read_file(json_file="results.json"):
        """Legge un file JSON e restituisce i dati."""
        try:
            with open(json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError: return []
        else: return []

class RFCExtractor:
    """Classe per l'estrazione dei numeri RFC dagli URL."""

    @staticmethod
    def extract_rfc_number(url):
        """Estrae il numero RFC dall'URL, se presente."""
        
        if "rfc-editor.org/rfc/rfc" in url:
            return url.removeprefix("https://www.rfc-editor.org/rfc/rfc").split('.')[0]
        
        if "rfc-editor.org/info/rfc" in url:
            return url.removeprefix("https://www.rfc-editor.org/info/rfc").split('.')[0]
        
        return None

    @staticmethod
    def get_rfc_params(results):
        """Estrae i numeri RFC dai risultati e tiene traccia della posizione migliore."""
        
        best_positions = {}
        
        position = 1
        for result in results:
            
            rfc_number = RFCExtractor.extract_rfc_number(result)
            if rfc_number and rfc_number not in best_positions:
                
                best_positions[rfc_number] = {"document_id": rfc_number, "position": position}
                position += 1
        
        return sorted(best_positions.values(), key=lambda x: x["position"])

class SearchEngineResultsProcessor:
    """Classe per gestire e processare i risultati dai motori di ricerca."""

    def __init__(self, max_results=30, alpha=1):
        self.max_results = max_results
        self.alpha = alpha
        self.results_by_engine = []

    def add_search_engine_results(self, engine_name, results):
        """Aggiunge i risultati di un motore di ricerca."""
        
        processed_results = RFCExtractor.get_rfc_params(results[:self.max_results])
        
        self.results_by_engine.append({
            "motore": engine_name,
            "documents": processed_results
        })
    
    def clear_search_engine_results(self):
        """ Pulisce i risultati dei motori di ricerca """
        
        self.results_by_engine.clear()

    def aggregate_scores(self):
        """Aggrega i punteggi di rilevanza basati su posizione e frequenza."""
        
        aggregati = {}
        
        for engine in self.results_by_engine:
            for doc in engine["documents"]:
                
                doc_id = doc["document_id"]
                position = doc["position"]
                score = self._calculate_score(position)
                
                if doc_id not in aggregati:
                    aggregati[doc_id] = {"document_id": doc_id, "total_score": 0, "frequency": 0}
                    
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
                "document_id": doc_id,
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

###################################################################################################

def process_queries(queries, processor):
    """Elabora le query e calcola i punteggi di rilevanza."""
    benchmark = []
    
    for query in queries:
        query_text = query.get("query")
        results = query.get("results", {})
        
        # Processa i risultati per ciascun motore di ricerca
        for engine, urls in results.items():
            random.shuffle(urls) # TODO: Levare Randomizzazione
            processor.add_search_engine_results(engine, urls) 
                    
        # Aggrega e calcola i punteggi delle posizioni
        aggregated_data = processor.aggregate_scores()
        final_scores = processor.calculate_final_relevance(aggregated_data)
        
        # Pulisce i risultati associati alla query corrente
        processor.clear_search_engine_results()
        
        # Appende il risultato finale alla lista del benchmark 
        benchmark.append({"query": query_text, "relevance_values": final_scores})
    
    return benchmark

def print_results(benchmark):
    """Stampa i risultati calcolati."""
    
    print("Query e relativi documenti con rilevanza calcolata:")
    for query in benchmark:
        
        query_text = query.get("query")
        print(f"\nTesto della Query: '{query_text}'")
        
        for score in query.get("relevance_values", []):
            
            print(
                f"Rfc: {score['document_id']}, ",
                f"Rilevanza: {score['relevance']:.5f}, ",
                f"Normalizzata: {score['normalized']:.5f}, ",
                f"Arrotondata: {score['rounded']}"
            )

def start():
    """Funzione principale per eseguire il calcolo dei punteggi di rilevanza."""
    
    # Configura il processore con i parametri desiderati
    processor = SearchEngineResultsProcessor(max_results=10, alpha=1)
    
    # Percorso del file JSON contenente le query
    queries_file_name = "results-for-testing.json" # TESTING
    #queries_file_name = "results.json"
    queries_file_path = os.path.join(os.path.dirname(__file__), queries_file_name)
    
    # Legge le query dal file JSON
    queries = RFCReader.read_file(queries_file_path)
    if not queries:
        print("Nessuna query trovata. Terminazione del programma.")
        return
    
    # Processa le query e calcola i punteggi di rilevanza
    benchmark = process_queries(queries, processor)
    
    # Stampa i risultati
    print_results(benchmark)
    
    # Ritorna il benchmark
    return benchmark

if __name__ == "__main__":
    start()