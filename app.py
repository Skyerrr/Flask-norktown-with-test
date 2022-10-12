import os
from typing import Type
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from src.models import db, Person
from src.views import routes


def create_app() -> Type[Flask]:
    """
    Create Flask app, Define Debug mode to True, Define app configs: Secret_key, Database, and disable track of objects to save memory.
    Initiate Flask app, initiate login manager and Return Flask object.
    """

    SECRET_KEY = os.urandom(32)
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///person.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(routes, url_prefix="")
    db.init_app(app)
    Bootstrap(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id) -> Type[Person]:
        """
        This sets the callback for reloading a user from the session.
        Return user Person object or None if the user does not exist.
        """

        return Person.query.get(int(user_id))

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
