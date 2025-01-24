from flask import Flask
import os
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.init_app(app)