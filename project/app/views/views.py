from flask import Blueprint, request, render_template

blueprint = Blueprint('views', __name__,
                  template_folder='../templates',
                  static_folder='../static')

@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/home', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        ...
        
    elif request.method == 'GET':
        return render_template('index.html')