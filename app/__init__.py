from flask import Flask
from profile.profile import profile
from routes.other_routes import other_routes
from auth.auth import auth
from app.database import db

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'whiskeys': 'sqlite:///whiskeys.sqlite'}

db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    # user = User.query.get(1)
    # db.session.delete(user)
    # db.session.commit()

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(other_routes, url_prefix='/other_routes')

