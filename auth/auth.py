from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User
from app.database import db


auth = Blueprint('auth', __name__, template_folder="templates")


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        password = request.form['password']
        if user_email == '' or password == '':
            flash('Please fill in all the required fields.')
            return redirect(url_for('login'))
        user = User.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user'] = user_email
                return redirect(url_for('home'))
            else:
                flash("Password is incorrect")
                return redirect(url_for('login'))
        else:
            flash("User does not exist")
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Log in')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        user_email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        check_box = request.form.get('checkbox')
        if username == '' or user_email == '' or phone == '' or password == '':
            flash('Please fill in all the required fields.')
            return redirect(url_for('signup'))
        elif not phone.isdecimal():
            flash('Phone must be a number')
            return redirect(url_for('signup'))
        elif check_box is None:
            flash('You must agree to the Terms of Service')
            return redirect(url_for('signup'))
        else:
            new_user = User(username=username, email=user_email, phone=phone, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user_email
            return redirect(url_for('home'))
    else:
        return render_template('signup.html', title='Sign up')


@auth.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))
