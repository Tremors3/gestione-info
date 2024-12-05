import numpy as np
import json

class RFCReader:
    """Classe per il recupero degli URL risultanti delle query."""
    
    @staticmethod
    def read_file(json_file="queries.json"):
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
        
        if "www.rfc-editor.org/info/rfc" in url:
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
                
                best_positions[rfc_number] = {"document_id": rfc_number, "posizione": position}
                position += 1
        
        return sorted(best_positions.values(), key=lambda x: x["posizione"])

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
            "documenti": processed_results
        })

    def aggregate_relevance(self):
        """Aggrega i punteggi di rilevanza basati su posizione e frequenza."""
        
        aggregati = {}
        
        for engine in self.results_by_engine:
            for doc in engine["documenti"]:
                
                doc_id = doc["document_id"]
                posizione = doc["posizione"]
                rilevanza = self._calculate_relevance(posizione)
                
                if doc_id not in aggregati:
                    aggregati[doc_id] = {"document_id": doc_id, "punteggio_totale": 0, "frequenza": 0}
                    
                aggregati[doc_id]["punteggio_totale"] += rilevanza
                aggregati[doc_id]["frequenza"] += 1
                
        return aggregati

    @staticmethod
    def _calculate_relevance(position):
        """Calcola il punteggio di rilevanza logaritmico basato sulla posizione."""
        
        return 1 / np.log2(position + 1)

    @staticmethod
    def normalize_scores(scores):
        """Normalizza i punteggi tra 0.0 e 2.0."""
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [2.0] * len(scores)
        
        return [2 * (score - min_score) / (max_score - min_score) for score in scores]

    def calculate_final_scores(self, aggregated_data):
        """Calcola i punteggi finali combinando posizione e frequenza."""
        
        documenti = []
        
        for doc_id, values in aggregated_data.items():
            punteggio_finale = values["punteggio_totale"] * (1 + self.alpha * values["frequenza"])
            documenti.append({
                "document_id": doc_id,
                "punteggio_rilevanza": punteggio_finale
            })
            
        if not documenti:
            raise ValueError("Non ci sono documenti per cui calcolare la rilevanza.")
        
        scores = [doc["punteggio_rilevanza"] for doc in documenti]
        normalized_scores = self.normalize_scores(scores)
        
        for i, doc in enumerate(documenti):
            doc["rilevanza_normalizzata"] = normalized_scores[i] + 1
            doc["rilevanza_normalizzata_arrotondata"] = round(normalized_scores[i]) + 1
            
        return documenti

###################################################################################################

def process_queries(queries, processor):
    """Elabora le query e calcola i punteggi di rilevanza."""
    benchmark = []
    
    for query in queries:
        query_text = query.get("query")
        results = query.get("results", {})
        
        # Processa i risultati per ciascun motore di ricerca
        for engine, urls in results.items():
            processor.add_search_engine_results(engine, urls)
        
        # Aggrega e calcola i punteggi di rilevanza
        aggregated_data = processor.aggregate_relevance()
        final_scores = processor.calculate_final_scores(aggregated_data)
        
        benchmark.append({"query": query_text, "scores": final_scores})
    
    return benchmark

def print_results(benchmark):
    """Stampa i risultati calcolati."""
    print("Query e relativi documenti con rilevanza calcolata:")
    for query in benchmark:
        query_text = query.get("query")
        print(f"\nQuery corrente: '{query_text}'")
        for score in query.get("scores", []):
            print(f"Rfc: {score['document_id']},\t",
                  f"Punteggio rilevanza: {score['punteggio_rilevanza']:.5f},\t\t",
                  f"Rilevanza normalizzata: {score['rilevanza_normalizzata']:.5f},\t",
                  f"Rilevanza normalizzata arrotondata: {score['rilevanza_normalizzata_arrotondata']}")

def main():
    """Funzione principale per eseguire il calcolo dei punteggi di rilevanza."""
    
    # Configura il processore con i parametri desiderati
    processor = SearchEngineResultsProcessor(max_results=20, alpha=1)
    
    # Legge le query dal file JSON
    queries = RFCReader.read_file("urls.json")
    if not queries:
        print("Nessuna query trovata. Terminazione del programma.")
        return
    
    # Processa le query e calcola i punteggi di rilevanza
    benchmark = process_queries(queries, processor)
    
    # Stampa i risultati
    print_results(benchmark)

if __name__ == "__main__":
    main()