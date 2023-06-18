from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'secretkey'


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        session['user'] = user_email
        return redirect(url_for('user', email=user_email))
    else:
        return render_template('login.html', title='Log in')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/user/<email>')
def user(email):
    if "user" in session:
        return render_template('user.html', email=email)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
