import os
from flask import Flask
from flask.ext.assets import Environment

from opencontracts import default_settings


EXPORTS_PATH = os.environ.get('TED_EXPORTS_PATH', 'ted_exports')
TED_USER = os.environ.get('TED_USER')
TED_PASSWORD = os.environ.get('TED_PASSWORD')
DATABASE = os.environ.get('TED_DATABASE_URL', 'sqlite:///ted.db')


app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('OPENCONTRACTS_SETTINGS', silent=True)

assets = Environment(app)
