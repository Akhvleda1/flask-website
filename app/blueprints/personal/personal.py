from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from app.models.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from database.database import db

personal = Blueprint('personal', __name__, static_folder='static', template_folder='templates')


@personal.route('/profile')
def profile():
    session.permanent = False
    user_email = session['user']
    user = User.query.filter_by(email=user_email).first()
    return render_template('personal/profile.html', user=user)


@personal.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        user_email = session['user']
        user = User.query.filter_by(email=user_email).first()

        current_password = request.form['current-password']
        new_password_first = request.form['new-password-first']
        new_password_second = request.form['new-password-second']
        actual_current_password = user.password

        if current_password == '' or new_password_first == '' or new_password_second == '':
            flash("Please fill in all the fields.")
            return redirect(url_for('personal.change_password'))

        if new_password_first != new_password_second:
            flash("New passwords do not match.")
            return redirect(url_for('personal.change_password'))

        if check_password_hash(actual_current_password, current_password):
            user.password = generate_password_hash(new_password_first)
            db.session.commit()
            flash('Password changed successfully')
            return redirect(url_for('personal.profile'))
        else:
            flash('Incorrect current password')
            return redirect(url_for('personal.change_password'))
    else:
        return render_template('personal/change-password.html')
