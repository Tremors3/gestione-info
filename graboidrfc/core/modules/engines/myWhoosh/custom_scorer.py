from whoosh.scoring import WeightingModel, BaseScorer
from datetime import date
from math import exp

class TF_IDF_FF(WeightingModel):
    
    def __init__(self, lambda_freshness=0.1):
        super().__init__()
        self.lambda_freshness = lambda_freshness
    
    def scorer(self, searcher, fieldname, text, qf=1):
        
        # Ottenimento del parent
        parent = searcher.get_parent()
        
        # Ottenimento dell'IDF (statico globalmente)
        idf = parent.idf(fieldname, text)

        # Punteggio massimo di peso per il termine
        maxweight = searcher.term_info(fieldname, text).max_weight()
        
        # Restituzione dello scorer
        return TF_IDF_FFScorer(maxweight, idf, searcher, self.lambda_freshness)

class TF_IDF_FFScorer(BaseScorer):
    def __init__(self, maxweight, idf, searcher, lambda_freshness):
        self._maxquality = maxweight * idf
        self.idf = idf
        self.searcher = searcher
        self.lambda_freshness = lambda_freshness

    def compute_freshness_factor(self, publication_date):
        """Calcola il fattore di freschezza in base alla data di pubblicazione"""
        # Ottenimento della data corrente
        current_date = date.today()
        
        # Calcolo della differenza in mesi tra la data di pubblicazione e la data corrente
        months_diff = (current_date.year - publication_date.year) * 12 + current_date.month - publication_date.month
        
        # Funzione esponezniale per il calcolo del fattore di freschezza
        freshness_factor = exp(-self.lambda_freshness * months_diff)
        
        # Restituzione freschezza
        return freshness_factor

    def supports_block_quality(self):
        return True

    def score(self, matcher):
        
        # Accediamo direttamente al docnum
        docnum = matcher.id()
        
        # Otteniamo i campi memorizzati tramite searcher
        stored_fields = self.searcher.stored_fields(docnum)
        
        # Otteniamo il campo data di pubblicazione
        publication_date = stored_fields.get("date")
        
        # Calcoliamo il fattore di freschezza
        freshness_factor = self.compute_freshness_factor(publication_date)
        
        # Restituiamo il TF x IDF x Fattore di Freschezza
        return matcher.weight() * self.idf * freshness_factor

    def max_quality(self):
        return self._maxquality

    def block_quality(self, matcher):
        return matcher.block_max_weight() * self.idf