from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'app.login'  # куда редиректить неавторизованных

    # регистрируем user_loader
    @login.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import bp
    app.register_blueprint(bp)

    return app
