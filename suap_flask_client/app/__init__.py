from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "supersecreto")
    app.config["SESSION_TYPE"] = "filesystem"

    Session(app)

    from .routes import main
    app.register_blueprint(main)

    return app