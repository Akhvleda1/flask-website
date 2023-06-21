from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whiskey_db.sqlite'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String)


cards = [
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 1',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 2',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 3',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 4',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 5',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 6',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 7',
        'description': 'This is the card.',
    },
    {
        'image': 'https://cdn.discordapp.com/attachments/1119903896115097668/1120416421692850246/generate_logo_for_Whiskey_with_t.png',
        'title': 'Card 7',
        'description': 'This is the card.',
    },

    # Add more card objects as needed
]


# def extract_name_from_email(email):
#     username, domain = email.split('@')
#
#     # Remove any dots from the username
#     username = username.replace('.', ' ')
#
#     # Split the username into parts
#     name_parts = username.split()
#
#     # Capitalize the first letter of each part and join them
#     name = ' '.join(part.capitalize() for part in name_parts)
#
#     return name


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop', cards=cards)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        password = request.form['password']
        if user_email == '' or password == '':
            flash('make sure to fill in all fields')
            return redirect(url_for('login'))
        session['user'] = user_email
        return redirect(url_for('home'))
    else:
        return render_template('login.html', title='Log in')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html', title='Sign up')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    user_email = session.get('user')
    if 'user' in session:
        return render_template('profile.html', email=user_email)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
