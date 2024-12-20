from flask import Flask
from flask_cors import CORS
from utils.db import db, init_db
from routes import register_routes
from config import (
    Config, Development
)

# backend builder
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    with app.app_context():
        init_db()

    register_routes(app)
    return app