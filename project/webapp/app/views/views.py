import json

# datetime
from datetime import date, timedelta, datetime

# Our Imports
from project.searchengine.myWhoosh.myWhoosh import process as processWhoosh

# Flask Utils for redirecting, blueprients, exc...
from flask import Blueprint, request, render_template, redirect, url_for, session

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, DateField, IntegerField, StringField, SubmitField, SelectField, TextAreaField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

class TermForm(FlaskForm):
    operator = SelectField('Operator', default='AND', choices=[('AND', 'AND'), ('OR', 'OR'), ('NOT', 'NOT')], render_kw={"id":"terms-operator"})
    term     = StringField('Term', validators=[], render_kw={"class":"input", "placeholder":"Search terms"})
    field    = SelectField(default='KEYWORDS', choices=[('TITLE', 'Title'), ('DESCRIPTION', 'Description'), ('KEYWORDS', 'Keywords')], render_kw={"id":"terms-field","class":"select"})

class SearchForm(FlaskForm):
    ############################################################ Ricerca Principale ############################################################
    ricerca_principale    = StringField('Ricerca principale', validators=[DataRequired()], render_kw={"class":"input","placeholder":"Ricerca","border-radius":"0"})
    ########################################################## Opzioni Ricerca Principale ######################################################
    spelling_correction   = BooleanField(label='Spelling Correction', validators=[], render_kw={"id":"spelling_correction",})
    synonims              = BooleanField(label='Sinonimi', validators=[], render_kw={"id":"synonims"})
    ######################################################## Selettore del searchengine ########################################################
    search_engine         = RadioField(default="WHOOSH", coerce=str, choices=[("WHOOSH", "Whoosh"),("PYLUCENE", "Pylucene"),("POSTGRESQL","PostgreSQL")])
    ############################################################## Stato dell'RFC ##############################################################
    standard_track        = BooleanField('Standard', render_kw={"id":"standard_track"})
    best_current_practice = BooleanField(label='Best current practice', render_kw={"id":"best_current_practice"})
    informational         = BooleanField(label='Informational', render_kw={"id":"informational"})
    experimental          = BooleanField(label='Experimental', render_kw={"id":"experimental"})
    historic              = BooleanField(label='Historic', render_kw={"id":"historic"})
    ######################################################## Valore di "standard track" ########################################################
    standard_track_value  = SelectField(default="PROPOSED_STANDARD", choices=[('PROPOSED_STANDARD', 'Proposed Standard'), ('DRAFT_STANDARD', 'Draft Standard'), ('INTERNET_STANDARD', 'Internet Standard')], render_kw={"id":"standard_track"})
    ############################################################## Selettore data ##############################################################
    date_year             = DateField(format='%Y',    render_kw={"id":"date_year",      "class":"input is-small", "type": "month", "placeholder":"YYYY"})
    date_from_date        = DateField(format='%Y-%m', render_kw={"id":"date_from_date", "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    date_to_date          = DateField(format='%Y-%m', render_kw={"id":"date_to_date",   "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    dates                 = RadioField(default="ALL_DATES", coerce=str, choices=[("ALL_DATES", "All Dates"),("SPECIFIC_YEAR", "Specific year"),("DATE_RANGE","Date Range")])
    ############################################################# Ternimi dinamici #############################################################
    terms                 = FieldList(FormField(TermForm), min_entries=0)
    ########################################################## Vogno o meno l'estratto ##########################################################
    abstracts             = RadioField(default="SHOW_ABSTRACTS", coerce=str, choices=[("SHOW_ABSTRACTS", "Show Abstracts"),("HIDE_ABSTRACTS", "Hide Abstracts")])
    ######################################################## Dimensione della richiesta ########################################################
    size                  = SelectField(default=25, coerce=int, choices=[(200, '200'), (100, '100'), (50, '50'), (25, '25')])
    ############################################################################################################################################
    submit                = SubmitField(render_kw={"class":"button is-link is-medium", "style":"margin-left: 0%; border-radius:0;"})
    ############################################################################################################################################

# Blueprint per le viste
blueprint = Blueprint('views', __name__,
                      template_folder = '../templates',
                      static_folder   = '../static')

# Route principale
@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':

        form = SearchForm()

        if form.is_submitted():

            # Parsa la form in json
            query = form_to_json(form, donot=('csrf_token', 'submit'))

            # Salva la query su file
            #save_query_to_file(query, "query.json")

            # Scelta del search engine
            if "WHOOSH" == query.get("search_engine"):
                response = processWhoosh(query)
                
            if "PYLUCENE" == query.get("search_engine"):
                pass #response = processPyLucene(query)
                
            if "POSTGRESQL" == query.get("search_engine"):
                pass #response = processPostgresql(query)
            
            # Print of the response
            # print(response)

            #session['search_results'] = json.dumps(response)
            session['search_results'] = response  # Flask lo serializza automaticamente

        return redirect(url_for('views.results'))

    if request.method == 'GET':

        return render_template('index.html', context={
            "form" : SearchForm()
        })

@blueprint.route('/results', methods=['GET'])
def results():
    
    if request.method == 'GET':
        
        results = json.loads(session.get('search_results', {}))
        
        # Aggiunta di altri campi
        for result in results:
            
            # Aggiunga Link
            result["link"] = f"https://rfc-editor.org/rfc/rfc{result.get('number')}"
            
            #Aggiunta Titolo
            result["link_title"] = f"RFC {result.get('number')}"
            
            # Mettere apposto links
            result["files"] = [f.lower().replace("text", "txt") for f in result['files'] if f not in ['HTML with inline errata']]

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

        return render_template('results.html', risultati=results, num_result=len(results), max_words=250)


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

        # Altrimenti, aggiungi direttamente il valore
        else:
            form_data[field_name] = field.data

    return form_data

# Funzione per salvare la query in un file JSON
def save_query_to_file(query: dict, filename: str):
    """Salva la query in un file JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(query, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Errore nel salvataggio del file {filename}: {e}")
