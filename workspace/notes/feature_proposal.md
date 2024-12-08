### [odea] PARALLELIZZAZIONE DEL PROCESSO DI DOWNLOAD E PARSING DELLE PAGINE WEB

Invece di utilizzare i thread in python. è melgio utilizzare processi perchè più efficienti.

### [idea] BENCHMARK

PROPOSTA LLM PER VERIFICARE LA CORRETTEZZA DEI DATI SULLA RILEVANZA (GIA' CALCOLATA) DEI DOCUMENTI DEL BENCHMARK
Una voltal eseguito lo script di creazione del benchmark otteniamo una lista di documenti con relativa rilevanza ad una data query. Invece di essere noi manualmente a fare un controllo sull'assegnazione della "Rilevanza Normalizzata Arrotondata" lo facciamo fare ad una LLVM addestrata?