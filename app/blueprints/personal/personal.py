from flask import Blueprint, session, render_template
from app.models.models import User

personal = Blueprint('personal', __name__, static_folder='static', template_folder='templates')


@personal.route('/profile')
def profile():
    user_email = session['user']
    user = User.query.filter_by(email=user_email).first()
    return render_template('personal/profile.html', user=user)
