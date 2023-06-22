from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'

db = SQLAlchemy(app)
conn = sqlite3.connect("whiskeys.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM whiskeys")
rows = cursor.fetchall()

nums = []
cards = []
names = []
prices = []
links = []
abouts = []

for row in rows:
    num = row[0]
    nums.append(num)

for row in rows:
    name = row[1]
    names.append(name)

for row in rows:
    price = row[2]
    prices.append(price)

for row in rows:
    link = row[3]
    links.append(link)

for row in rows:
    about = row[4]
    abouts.append(about)

x = 0
while x <= 51:
    card = {
        'id': nums[x],
        'name': names[x],
        'image': links[x],
        'price': prices[x],
        'about': abouts[x]
    }
    cards.append(card)
    x += 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


with app.app_context():
    # db.drop_all()
    db.create_all()

# cards = [
#     {
#         'id': 1,
#         'image': 'https://img.thewhiskyexchange.com/900/irish_gre9.jpg',
#         'title': 'Card 1',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 2,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 2',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 3,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 3',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 4,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 4',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 5,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 5',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 6,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 6',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 7,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 7',
#         'price': '$40.00 - $80.00',
#     },
#     {
#         'id': 8,
#         'image': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
#         'title': 'Card 8',
#         'price': '$40.00 - $80.00',
#     },
#     # Add more card objects as needed
# ]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about/item_id=<int:item_id>')
def about_item(item_id):
    # Retrieve the item based on the provided ID
    item = next((card for card in cards if card['id'] == item_id), None)
    if item:
        return render_template('about.html', title='About Item', item=item)
    else:
        return redirect(url_for('shop'))


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
