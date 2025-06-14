
# imports
import os, uuid, json, ast

# datetime
from datetime import date, timedelta, datetime

# #################################################################################################### #

# Importazione moduli di progetto
from graboidrfc.core.modules.engines.myWhoosh.myWhoosh import MyWhoosh
from graboidrfc.core.modules.engines.myPostgres.myPostgres import MyPostgres
from graboidrfc.core.modules.engines.myPylucene.myPylucene import MyPyLucene
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors

# #################################################################################################### #

# Flask Utils for redirecting, blueprients, exc...
from flask import Blueprint, request, render_template, redirect, url_for, current_app

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, DateField, IntegerField, StringField, SubmitField, SelectField, TextAreaField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Regexp

# #################################################################################################### #

# Validatore per il formato delle date
def validate_date_format_month(form, field):
    if field.data:
        try: datetime.strptime(field.data.strftime('%Y-%m'), '%Y-%m')
        except ValueError:
            raise ValidationError("La data deve essere nel formato YYYY-MM (esempio: 2023-12).")

# Validatore per il formato delle date
def validate_date_format_year(form, field):
    if field.data:
        try: datetime.strptime(field.data.strftime('%Y'), '%Y')
        except ValueError:
            raise ValidationError("La data deve essere nel formato YYYY (esempio: 2023).")

# #################################################################################################### #

class RankingOption:

    FUNCTIONS = {
        
        "whoosh": {
            # BM25
            "BM25": "BM25",
            "BM25_CUSTOM": "BM25 Custom",
            # VSM
            "VSM": "VSM (TF-IDF)",
            "VSM_CUSTOM": "VSM Custom (TF-IDF-FF)",
        },
        
        "pylucene": {
            # BM25
            "BM25": "BM25",
            "BM25_CUSTOM": "BM25 Custom",
            # VSM
            "VSM": "VSM (TF-IDF)",
            "VSM_CUSTOM": "VSM Custom (TFLN-PIDF)"
        },
        
        "postgresql": {
            # Coverage Density
            "CD": "Coverage Density",
            "CD_CUSTOM": "Coverage Density Custom (DLN)",
            # Statistical Weighting
            "SW": "Statistical Weighting",
            "SW_CUSTOM": "Statistical Weighting Custom (DLN)",
        },
    }
    
    @staticmethod
    def get_choices(engine: str):
        return [(field, value) for field, value in __class__.FUNCTIONS.get(engine, {}).items()]
    
class TermForm(FlaskForm):
    operator = SelectField('Operator', default='AND', choices=[('AND', 'AND'), ('OR', 'OR'), ('NOT', 'NOT')], render_kw={"id":"terms-operator"})
    term     = StringField('Term', validators=[], render_kw={"class":"input", "placeholder":"Search terms"})
    field    = SelectField(default='KEYWORDS', choices=[('TITLE', 'Title'), ('ABSTRACT', 'Description'), ('KEYWORDS', 'Keywords')], render_kw={"id":"terms-field","class":"select"})

class SearchForm(FlaskForm):
    ############################################################ Ricerca Principale ############################################################
    ricerca_principale    = StringField('Ricerca principale', validators=[DataRequired()], render_kw={"class":"input","placeholder":"Ricerca","border-radius":"0"})
    ########################################################## Opzioni Ricerca Principale ######################################################
    spelling_correction   = BooleanField(label='Spelling Correction', validators=[], render_kw={"id":"spelling_correction",})
    synonims              = BooleanField(label='Sinonimi', validators=[], render_kw={"id":"synonims"})
    ######################################################## Selettore del searchengine ########################################################
    search_engine         = RadioField(default="WHOOSH", coerce=str, choices=[("WHOOSH", "Whoosh"),("PYLUCENE", "Pylucene"),("POSTGRESQL","PostgreSQL"),("TUTTI","All")])
    whoosh_ranking        = SelectField(default="BM25F", coerce=str, choices=RankingOption.get_choices("whoosh"))
    pylucene_ranking      = SelectField(default="RankingPyLucene_1", coerce=str, choices=RankingOption.get_choices("pylucene"))
    postgresql_ranking    = SelectField(default="RankingPostgreSQL_1", coerce=str, choices=RankingOption.get_choices("postgresql"))
    ############################################################## Stato dell'RFC ##############################################################
    standard_track        = BooleanField('Standard', render_kw={"id":"standard_track"})
    best_current_practice = BooleanField(label='Best current practice', render_kw={"id":"best_current_practice"})
    informational         = BooleanField(label='Informational', render_kw={"id":"informational"})
    experimental          = BooleanField(label='Experimental', render_kw={"id":"experimental"})
    historic              = BooleanField(label='Historic', render_kw={"id":"historic"})
    ######################################################## Valore di "standard track" ########################################################
    standard_track_value  = SelectField(default="PROPOSED_STANDARD", choices=[('PROPOSED_STANDARD', 'Proposed Standard'), ('DRAFT_STANDARD', 'Draft Standard'), ('INTERNET_STANDARD', 'Internet Standard')], render_kw={"id":"standard_track"})
    ############################################################## Selettore data ##############################################################
    date_year             = IntegerField(validators=[Regexp(r'^\d{4}$', message="Deve essere un anno valido (4 cifre)")],  render_kw={"id":"date_year", "class":"input is-small", "type": "number", "placeholder":"YYYY", "min": 1900, "max": datetime.now().year})
    date_from_date        = DateField(format='%Y-%m', render_kw={"id":"date_from_date", "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    date_to_date          = DateField(format='%Y-%m', render_kw={"id":"date_to_date",   "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    dates                 = RadioField(default="ALL_DATES", coerce=str, choices=[("ALL_DATES", "All Dates"),("SPECIFIC_YEAR", "Specific year"),("DATE_RANGE","Date Range")])
    ############################################################# Ternimi dinamici #############################################################
    terms                 = FieldList(FormField(TermForm), min_entries=0)
    ########################################################## Vogno o meno l'estratto ##########################################################
    abstracts             = RadioField(default="True", coerce=str, choices=[("True", "Show Abstracts"),("False", "Hide Abstracts")])
    ######################################################## Dimensione della richiesta ########################################################
    size                  = SelectField(default=25, coerce=int, choices=[(200, '200'), (100, '100'), (50, '50'), (25, '25')])
    ############################################################################################################################################
    submit                = SubmitField(render_kw={"class":"button is-link is-medium", "style":"margin-left: 0%; border-radius:0;"})
    ############################################################################################################################################

# #################################################################################################### #

# Blueprint per le viste
blueprint = Blueprint('views', __name__,
                      template_folder = '../templates',
                      static_folder   = '../static')

# #################################################################################################### #

# Percorsi files e cartelle
DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_DIR_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "data", "tmp")

os.makedirs(CURRENT_TEMP_DIR_PATH, exist_ok=True)

# #################################################################################################### #

@blueprint.before_request
def before_request():
    MyPyLucene.init_lucene_vm()
    MyPyLucene.attach_lucene_to_thread()
    pass

# Route principale
@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':

        form = SearchForm()

        if form.is_submitted():

            # Parsa la form in json
            query = form_to_json(form, donot=('csrf_token', 'submit'))

            # Default response vuota
            response = {}
            
            # Valori per il salvataggio
            result_id = str(uuid.uuid4())
            file_path = f"{result_id}.json"
            
            # Quale search engine utilizzare
            chosen_se = query.get("search_engine") 
            
            # Usa tutti i Search Engine
            tutti = False 
            
            # Modello di ranking scelto per ogni S.E.
            ranking_models = {
                "whoosh": query.get("whoosh_ranking"),
                "pylucene": query.get("pylucene_ranking"),
                "postgresql": query.get("postgresql_ranking"),
            }

            # Scelta del search engine
            if "WHOOSH" == chosen_se:
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyWhoosh.process(query)
                save_results_to_file(response, file_path)
                
            if "PYLUCENE" == chosen_se:
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyPyLucene.process(query)
                save_results_to_file(response, file_path)
            
            if "POSTGRESQL" == chosen_se:
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyPostgres(use_docker=current_app.config.get("USE_DOCKER", False)).process(query)
                save_results_to_file(response, file_path)

            if "TUTTI" == chosen_se:
                tutti = True
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyWhoosh.process(query)
                save_results_to_file(response, f"WHOOSH{file_path}")
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyPyLucene.process(query)
                save_results_to_file(response, f"PYLUCENE{file_path}")
                # Ottiene e salva i risultati su file per essere recuperati alla richiesta
                response = MyPostgres(use_docker=current_app.config.get("USE_DOCKER", False)).process(query)
                save_results_to_file(response, f"POSTGRESQL{file_path}")
            
            return redirect(url_for('views.results', result_id=result_id, chosen_se=chosen_se, tutti=tutti, ranking_models=ranking_models, show_abstracts=query.get('abstracts')))

        return redirect(url_for('views.results', result_id=None, show_abstracts=None))

    if request.method == 'GET':

        return render_template('index.html', context={
            "form" : SearchForm()
        })

# #################################################################################################### #

@blueprint.route('/results', methods=['GET'])
def results():
    
    if request.method == 'GET':
        
        # Valori per il recupero
        result_id = request.args.get('result_id', None)
        tutti = True if request.args.get('tutti', False) == "True" else False
        ranking_models = ast.literal_eval(request.args.get("ranking_models"))
        
        if tutti:
            
            # Tre motori di ricerca
            engines = ["whoosh", "pylucene", "postgresql"]
            
            # Dizionario per i risultati
            search_engines = {}
            
            for engine in engines:
                
                # Nome del file temporaneo
                file_path = f"{engine.upper()}{result_id}.json"
            
                # Ritiro dei risultati
                results = load_results_from_file(file_path)
                
                # Cancellazione del file temporaneo dopo il recupero
                delete_file(file_path)

                # Parsing dei risultati
                results = results_parser(results)
                
                # Ottenimento del modello di ranking selezionato
                ranking_model = RankingOption.FUNCTIONS.get(engine).get(ranking_models.get(engine))

                # Aggiunta dei risultati
                search_engines[engine] = {
                    "results": results,
                    "num_result": len(results),
                    "ranking_model": ranking_model
                }
            
            return render_template('results_tutti.html', max_words=250, search_engines=search_engines)
        
        # Nome del file temporaneo
        file_path = f"{result_id}.json"
        
        # Ritiro dei risultati
        results = load_results_from_file(file_path)
        
        # Cancellazione del file dopo il recupero
        delete_file(file_path)
        
        # Parsing rei risultati
        results = results_parser(results)

        # Search engine utilizzato
        chosen_se = request.args.get("chosen_se").lower()

        # Modello di ranking selezionato
        ranking_model = RankingOption.FUNCTIONS.get(chosen_se).get(ranking_models.get(chosen_se))

        return render_template('results.html', max_words=250, chosen_se=chosen_se, ranking_model=ranking_model, risultati=results, num_result=len(results))

def results_parser(results: list[dict]):
    
    for result in results:
        # Aggiunta Link
        result["link"] = f"https://rfc-editor.org/rfc/rfc{result.get('number')}"
        #Aggiunta Titolo
        result["link_title"] = f"RFC {result.get('number')}"
        # Eventuale rimozione degli abstracts
        if request.args.get('show_abstracts', "True") == "False":
            del result["abstract"]
    
    return results

# risultati = [
#     {
#         "link":"https://rfc-editor.org/rfc/rfc9000",
#         "link_title":"RFC 9000",
#         "title":"Qualcosa qualcosa 1",
#         "formats":["pdf","html","txt"],
#         "authors": ["Autore 1","Autore 2","Autore 3","Autore 4"],
#         "date": "1111/11/11",
#         "comment": "commento",
#         "abstract":"Estratto della pagina dell'rfc 9000"
#     }
# ]

# #################################################################################################### #

# Funzione per formattare la query
def form_to_json(form: FlaskForm, donot: set[str]):

    form_data = {}

    for field_name, field in form._fields.items():

        # Alcuni campi non li accettiamo
        if field_name in donot: continue

        # Se il campo è un FieldList, estrai i dati dai suoi subfield
        if isinstance(field, FieldList):

            subfields = []
            for subfield in field.entries:

                subfield_dict = {}
                for subfield_name, subfield in subfield._fields.items():
                    if not 'csrf' in subfield_name:
                        subfield_dict[subfield_name] = subfield.data

                # Appendiamo solamente se il subfield non è vuoto
                if len(subfield_dict['term']):
                    subfields.append(subfield_dict)

            # Aggiungiamo i termini aggiuntivi (per ultimi)
            form_data[field_name] = subfields

        # Se il campo è un DateField, formattalo "anno-mese"
        elif isinstance(field, DateField):
            form_data[field_name] = field.data.strftime('%Y-%m') if field.data else None

        # Altrimenti, aggiungi direttamente il valore
        else: form_data[field_name] = field.data

    return form_data

# #################################################################################################### #

# Funzioni di gestione dei file temporanei
def save_results_to_file(results: dict, filename: str):
    """Salva i risultati in un file JSON nel directory temporaneo."""
    try:
        filepath = os.path.join(CURRENT_TEMP_DIR_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"Errore nel salvataggio del file {filepath}: {e}")

def load_results_from_file(filename: str):
    """Carica i risultati da un file JSON nel directory temporaneo."""
    try:
        filepath = os.path.join(CURRENT_TEMP_DIR_PATH, filename)
        if not os.path.isfile(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Errore nella lettura del file {filepath}: {e}")
        return []

def delete_file(filename: str):
    """Cancella un file JSON nel directory temporaneo."""
    try:
        filepath = os.path.join(CURRENT_TEMP_DIR_PATH, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except IOError as e:
        logging.error(f"Errore nella cancellazione del file {filepath}: {e}")