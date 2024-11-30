from flask import Blueprint, request, render_template, redirect, url_for
from datetime import datetime
from pprint import pprint
import json

blueprint = Blueprint('views', __name__,
                  template_folder='../templates',
                  static_folder='../static')

@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
           
        query: dict = format_query(request.form)

        with open("temp.json", "w", encoding="utf-8") as f:
            json.dump(query, f, ensure_ascii=False, indent=4)

        return redirect('/')
    
    elif request.method == 'GET':
        return render_template('index.html')

def format_query(form) -> dict: 
    
    # Parse the Form
    jsonified = {
        # Ricerca Principale
        "ricerca_principale"    : form.get('ricerca_principale', ""),
        # Opzioni della ricerca - Checkboxes
        "spelling_correction"   : True if form.get('spelling_correction', False) else False,
        "synonims"              : True if form.get('synonims', False) else False,
        # Stato - Checkboxes
        "standard_track"        : True if form.get('standard', False) else False,
        "best_current_practice" : True if form.get('best_current_practice', False) else False,
        "informational"         : True if form.get('informational', False) else False,
        "experimental"          : True if form.get('experimental', False) else False,
        "historic"              : True if form.get('historic', False) else False,
        # Valore di "standard track"
        # PROPOSED_STANDARD - Proposed Standard
        # DRAFT_STANDARD    - Draft Standard
        # INTERNET_STANDARD - Internet Standard
        "standard"              : form.get('standard_track', "PROPOSED_STANDARD"), # STANDARD E STANDARD_TRACK SONO INVERTITI
        # Date - Radiobutton
        # ALL_DATES         - All dates
        # SPECIFIC_YEAR     - Specific dates
        # DATE_RANGE        - Date range
        "date-filter_by"        : form.get('date-filter_by', "ALL_DATES"),
        # Anno Specifico
        "date-year"             : form.get('date-year', "") if check_date(form.get('date-year', "")) else "",
        # Range delle Date
        "date-from_date"        : form.get('date-from_date',  "") if check_date(form.get('date-from_date', "")) else "",
        "date-to_date"          : form.get('date-to_date', "") if check_date(form.get('date-to_date', "")) else "",
        # Abstract - Radiobutton
        "abstracts"             : True if form.get('abstracts') == 'True' else False,
        # Dimensione richiesta
        "size"                  : int(form.get('size', 25))
    }
    
    # Parse Query Terms
    jsonified["terms"] = format_terms(form)
    
    return jsonified

def format_terms(form) -> list[dict]:
    
    terms = []
    for i in range(0,int(form['numero_terms'])+1):
        try:
            terms.append({
                # Operatore
                # AND
                # OR
                # NOT
                "operator": form.get(f"terms-{i}-operator", "AND"),
                # Termine
                "term"    : form.get(f"terms-{i}-term", ""),
                # Filed of research
                # TITLE
                # KEYWORD
                # AUTHOR
                "field"   : form.get(f"terms-{i}-field")
            })
        except Exception as ignore: pass
    return terms
    
def check_date(check):
    if not check: return check
    try: return bool(datetime.strptime(check, "%Y-%m"))
    except Exception: return ""