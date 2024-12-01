from flask import Blueprint, request, render_template, redirect, url_for
from datetime import datetime
import json

# Blueprint per le viste
blueprint = Blueprint('views', __name__,
                      template_folder='../templates',
                      static_folder='../static')

# Route principale
@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # Format query and save to file
        query = format_query(request.form)
        save_query_to_file(query, "query.json")
        return redirect('/')
    return render_template('index.html')

# Funzione per formattare la query
def format_query(form) -> dict:
    """Parsa e valida i dati inviati tramite il form."""
    return {
        # Ricerca principale
        "ricerca_principale": form.get('ricerca_principale', "").strip(),
        
        # Opzioni di ricerca (checkbox)
        "spelling_correction": bool(form.get('spelling_correction')),
        "synonims": bool(form.get('synonims')),
        
        # Search engine
        "search_engine": form.get('search_engine', 'WHOOSH'),

        # Stato (checkbox)
        "standard_track": bool(form.get('standard')),
        "best_current_practice": bool(form.get('best_current_practice')),
        "informational": bool(form.get('informational')),
        "experimental": bool(form.get('experimental')),
        "historic": bool(form.get('historic')),
        
        # Valore di "standard track"
        "standard": form.get('standard_track', "PROPOSED_STANDARD").strip(),
        
        # Filtro per data
        "date-filter_by": form.get('date-filter_by', "ALL_DATES").strip(),
        "date-year": validate_date(form.get('date-year')),
        "date-from_date": validate_date(form.get('date-from_date')),
        "date-to_date": validate_date(form.get('date-to_date')),
        
        # Abstracts (radiobutton)
        "abstracts": form.get('abstracts') == 'True',
        
        # Dimensione richiesta
        "size": safe_cast(form.get('size'), int, 25),
        
        # Termini di ricerca
        "terms": format_terms(form)
    }

# Funzione per formattare i termini di ricerca
def format_terms(form) -> list[dict]:
    """Estrae e valida i termini di ricerca dal form."""
    terms = []
    numero_terms = safe_cast(form.get('numero_terms'), int, 0)
    for i in range(numero_terms + 1):
        term_data = {
            "operator": form.get(f"terms-{i}-operator", "AND").strip(),
            "term": form.get(f"terms-{i}-term", "").strip(),
            "field": form.get(f"terms-{i}-field", "TITLE").strip()
        }
        if term_data["term"]:  # Aggiungi solo termini validi
            terms.append(term_data)
    return terms

# Funzione per validare una data (YYYY-MM)
def validate_date(date_str: str) -> str:
    """Valida il formato della data (YYYY-MM)."""
    if not date_str:
        return ""
    try:
        datetime.strptime(date_str, "%Y-%m")
        return date_str
    except ValueError:
        return ""

# Funzione per salvare la query in un file JSON
def save_query_to_file(query: dict, filename: str):
    """Salva la query in un file JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(query, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Errore nel salvataggio del file {filename}: {e}")

# Funzione per eseguire il casting sicuro di un valore
def safe_cast(value, to_type, default):
    """Esegue il casting di un valore con un valore di default in caso di errore."""
    try:
        return to_type(value)
    except (ValueError, TypeError):
        return default