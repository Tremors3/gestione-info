import json

# datetime
from datetime import date, timedelta, datetime

# Flask Utils for redirecting, blueprients, exc...
from flask import Blueprint, request, render_template, redirect, url_for

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, DateField, IntegerField, StringField, SubmitField, SelectField, TextAreaField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

class TermForm(FlaskForm):
    operator = SelectField('Operator', choices=[('AND', 'AND'), ('OR', 'OR')], default='AND')
    term     = StringField('Term', validators=[DataRequired()], render_kw={"class":"input", "placeholder":"Search terms"})
    field    = SelectField(default='TITLE', choices=[('TITLE', 'Title'), ('DESCRIPTION', 'Description')])

class SearchForm(FlaskForm):
    # Ricerca Principale
    ricerca_principale    = StringField('Ricerca principale', validators=[DataRequired()], render_kw={"class":"input","placeholder":"Ricerca","border-radius":"0"})
    # Opzioni Ricerca Principale
    spelling_correction   = BooleanField(label='Spelling Correction', validators=[], render_kw={"id":"spelling_correction",})
    synonims              = BooleanField(label='Sinonimi', validators=[], render_kw={"id":"synonims"})
    # Selettore del search engine
    search_engine         = RadioField(default="WHOOSH", coerce=str, choices=[("WHOOSH", "Whoosh"),("PYLUCENE", "Pylucene"),("POSTGRESQL","PostgreSQL")])
    # Stato dell'RFC
    standard_track        = BooleanField('Standard', render_kw={"id":"standard_track"})
    best_current_practice = BooleanField(label='Best current practice', render_kw={"id":"best_current_practice"})
    informational         = BooleanField(label='Informational', render_kw={"id":"informational"})
    experimental          = BooleanField(label='Experimental', render_kw={"id":"experimental"})
    historic              = BooleanField(label='Historic', render_kw={"id":"historic"})
    # Valore di "standard track"
    standard_track_value  = SelectField(default="PROPOSED_STANDARD", choices=[('PROPOSED_STANDARD', 'Proposed Standard'), ('DRAFT_STANDARD', 'Draft Standard'), ('INTERNET_STANDARD', 'Internet Standard')], render_kw={"id":"standard_track"})
    # Selettore data
    date_year             = DateField(format='%Y',    render_kw={"id":"date_year",      "class":"input is-small", "type": "month", "placeholder":"YYYY"})
    date_from_date        = DateField(format='%Y-%m', render_kw={"id":"date_from_date", "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    date_to_date          = DateField(format='%Y-%m', render_kw={"id":"date_to_date",   "class":"input is-small", "type": "month", "placeholder":"YYYY[-MM]"})
    dates                 = RadioField(default="ALL_DATES", coerce=str, choices=[("ALL_DATES", "All Dates"),("SPECIFIC_YEAR", "Specific year"),("DATE_RANGE","Date Range")])
    # Ternimi dinamici
    # numero_terms          = IntegerField(default=0, render_kw={"id":"numero_terms","class":"input", "width": "0px", "height": "0px", "visibility": "hidden", "margin": "0px", "padding": "0px"})
    terms                 = FieldList(FormField(TermForm), min_entries=1)
    # Vogno o meno l'estratto
    abstracts             = RadioField(default="SHOW_ABSTRACTS", coerce=str, choices=[("SHOW_ABSTRACTS", "Show Abstracts"),("HIDE_ABSTRACTS", "Hide Abstracts")])
    # Dimensione della richiesta
    size                  = SelectField(default=25, coerce=int, choices=[(200, '200'), (100, '100'), (50, '50'), (25, '25')])
    submit                = SubmitField(render_kw={"class":"button is-link is-medium", "style":"margin-left: 0%; border-radius:0;"})

#class FilterForm(FlaskForm):
#    nome            = StringField(validators  = [Length(min=4, max=64)],  render_kw={"placeholder":"Ricerca per nome", "class":"form-control mr-1"})
#    min_price       = IntegerField(validators = [InputRequired()], render_kw={"placeholder":"min_price", "type": "number", "class":"input-min form-control", "value": "25"})
#    max_price       = IntegerField(validators = [InputRequired()], render_kw={"placeholder":"max_price", "type": "number", "class":"input-max form-control", "value":"750"})
#    min_price_range = IntegerField(validators = [InputRequired()], render_kw={"placeholder":"min_price", "type": "range", "class":"range-min", "min":"0", "max": "1000", "value": "200", "step":"10"})
#    max_price_range = IntegerField(validators = [InputRequired()], render_kw={"placeholder":"max_price", "type": "range", "class":"range-max", "min":"0", "max": "1000", "value": "750", "step":"10"})
#    camere          = IntegerField(validators = [], render_kw={"placeholder":"N° camere", "class":"form-control"})
#    bagni           = IntegerField(validators = [], render_kw={"placeholder":"N° bagni", "class":"form-control"})
#    persone         = IntegerField(validators = [], render_kw={"placeholder":"N° persone", "class":"form-control"})
#    sauna           = BooleanField(label="Sauna", render_kw={"id": "_checkbox1", "class":"form-control w-50"})
#    animali         = BooleanField(label="Sono amessi gli animali?", render_kw={"id": "_checkbox2", "class":"form-control w-50"})
#    check_in        = DateField('Data Inizio', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()], render_kw={"id":"check-in", "class": "data-input"})
#    check_out       = DateField('Data Fine', format='%Y-%m-%d', default=date.today() + timedelta(days = 7), validators=[DataRequired()], render_kw={"id":"check-out", "class": "data-input ml-2"})
#    radio_stars     = RadioField('Filtro Stelle', coerce=int, choices=[(5, 'Five Stars'), (4,'Four Stars'), (3,'Three Stars'), (2,'Two Stars'), (1,'One Star')])
#    submit          = SubmitField("Cerca",  render_kw={"id": "search-button", "class":"btn btn-primary btn-block ml-2", "style":"background-color: #007bff; color: #fff;"})

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
        
        if form.is_submitted(): # form.validate_on_submit() and
        
            # Elenco dei termini di ricerca
            terms = []
            for term_form in form.terms.entries:
                if not term_form.term.data is None and not term_form.term.data == '':
                    terms.append({
                        'operator': term_form.operator.data,
                        'term'    : term_form.term.data,
                        'field'   : term_form.field.data
                    })
            
            query = {}
            #query = field2dict(form)
            query['terms'] = terms  # Aggiungi i termini dinamici alla query
        
            from pprint import pprint
            
            pprint(query)
            pprint(form.dates.data)
            pprint(form.date_year.data)
            pprint(form.date_from_date.data)
            pprint(form.date_to_date.data)
            
            save_query_to_file(query, "query.json")
        
        return redirect(url_for('views.results'))
    
    if request.method == 'GET':
    
        return render_template('index_flaskwtf.html', context={
            "form" : SearchForm()
        })


@blueprint.route('/results', methods=['GET'])
def results():
    if request.method == 'GET':
        return render_template('results.html')


# Funzione per salvare la query in un file JSON
def save_query_to_file(query: dict, filename: str):
    """Salva la query in un file JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(query, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Errore nel salvataggio del file {filename}: {e}")


def field2dict(field):
    dict = {}
    for column in field.__table__.columns:
        #dict[column.name] = str(getattr(row, column.name))
        dict[column.name] = getattr(field, column.name)
    return dict

def rows2dict(rows):
    list = []
    for row in rows:
        dict = {}
        for column in row.__table__.columns:
            #dict[column.name] = str(getattr(row, column.name))
            dict[column.name] = getattr(row, column.name)
        list.append(dict)
    return list