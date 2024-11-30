from flask import Blueprint, request, render_template, redirect, url_for
from pprint import pprint

blueprint = Blueprint('views', __name__,
                  template_folder='../templates',
                  static_folder='../static')

@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/search', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        
        

        query = {}    
        query = jsonify(request.form)



        return redirect('/')
    
    elif request.method == 'GET':
        return render_template('index.html')

def jsonify(to_be_jsonified) -> dict: 
    jsonified = {}

    if (len(request.form['ricerca_principale'])):
            for i in range(0,int(request.form['numero_terms'])+1):
                try:
                    jsonified[]
                    print(f"{i} - Operator:", request.form[f"terms-{i}-operator"],"-- Term:", request.form[f"terms-{i}-term"],"-- Field:", request.form[f"terms-{i}-field"])
                except Exception:
                    ...