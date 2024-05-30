from flask import Blueprint, session, render_template
from models.models import User

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/profile')
def profile():
    user_email = session['user']
    user = User.query.filter_by(email=user_email).first()
    return render_template(' profile.html', user=user)
