from flask import Blueprint, render_template

blueprint = Blueprint('handlers', __name__,
                     template_folder='../templates',
                     static_folder='../static')

# Invalid URL: "Page Not Found"
@blueprint.errorhandler(404)
def page_not_found(ignore):
    return render_template('404.html'), 404

# Internal Server Error: "The Server Had an Internal Error"
@blueprint.errorhandler(500)
def page_not_found(ignore):
    return render_template('500.html'), 500