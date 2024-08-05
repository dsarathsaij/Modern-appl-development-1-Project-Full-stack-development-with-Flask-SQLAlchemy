from flask import Flask
from backend.db import db
from backend.res import apis

app = None

def log_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydata.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    apis.init_app(app)
    app.secret_key = 'itsmywish'
    app.app_context().push()
    return app

app = log_app()

from backend.control import *

if __name__ == "__main__":
    app.run(debug=True)
    
