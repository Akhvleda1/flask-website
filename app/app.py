from flask import Flask, session
from database.database import db
from datetime import timedelta
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretkey'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///user_db.sqlite'
    app.config['SQLALCHEMY_BINDS'] = {'whiskeys': f'sqlite:///whiskeys.sqlite'}

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # import and register blueprints
    from app.blueprints.auth.auth import auth
    from app.blueprints.personal.personal import personal
    from app.blueprints.routes.routes import routes
    from app.blueprints.core.core import core

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(personal, url_prefix='/personal')
    app.register_blueprint(routes, url_prefix='/routes')
    app.register_blueprint(core, url_prefix='/')

    return app

