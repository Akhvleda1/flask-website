from flask import Blueprint, render_template

core = Blueprint('core', __name__, static_folder='static', template_folder='templates')


@core.route('/')
@core.route('/home')
def home():
    return render_template('core/home.html')
