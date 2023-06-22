from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


with app.app_context():
    # db.drop_all()
    db.create_all()

cards = [
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    {
        'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
        'title': 'Card 1',
        'price': '$40.00 - $80.00',
    },
    # Add more card objects as needed
]


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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        user_email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        if username == '' or user_email == '' or phone == '' or password == '':
            flash('Please fill in all the required fields.')
            return redirect(url_for('signup'))
        elif not phone.isdecimal():
            flash('Phone must be a number')
            return redirect(url_for('signup'))
        else:
            new_user = User(username=username, email=user_email, phone=phone, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user_email
            return redirect(url_for('home'))
    else:
        return render_template('signup.html', title='Sign up')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # user_email = session.get('user')
    # if 'user' in session:
    #     return render_template('profile.html', email=user_email)
    # else:
    #     return redirect(url_for('login'))

    user_email = session['user']
    user = User.query.filter_by(email=user_email).first()
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
