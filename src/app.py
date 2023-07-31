import os

from flask import Flask
from extensions import api
from dotenv import load_dotenv
from views import ns

load_dotenv()

app = Flask(__name__)

app.config['ERROR_INCLUDE_MESSAGE'] = os.environ.get('ERROR_INCLUDE_MESSAGE')
api.init_app(app)
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(
        debug = os.environ.get('DEBUG'), 
        host = os.environ.get('HOST'), 
        port = os.environ.get('PORT')
        )