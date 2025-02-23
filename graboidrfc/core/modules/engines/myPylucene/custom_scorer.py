from org.apache.lucene.search.similarities import SimilarityBase, ClassicSimilarity
from datetime import date

class VSM_CUSTOM(SimilarityBase):
    
    def __init__(self):
        self.vsm = ClassicSimilarity()
        
    def compute_factor(self):
        """Funzione che restituisce il fattore personalizzato"""
        return 1

    def score(self, stats, freq, docLen):
        
        # Otteniamo il punteggio calcolato tramite VSM
        vsm_score = self.vsm.score(stats, freq, docLen)
        
        # Calcoliamo il fattore personalizzato
        custom_factor = self.compute_factor()
        
        # Restituiamo Rilevanza Doc x Fattore Custom
        return vsm_score * custom_factor
    
    def toString(self):
        return "VSM_CUSTOM_Similarity"