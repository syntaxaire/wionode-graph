from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app import routes, models
