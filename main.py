from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'secretkey'

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
        session['user'] = user_email
        return redirect(url_for('user', email=user_email))
    else:
        return render_template('login.html', title='Log in')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # if request.form = 'POST':

    return render_template('signup.html', title='Sign up')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/user/<email>')
def user(email):
    if "user" in session:
        return render_template('user.html', email=email)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
