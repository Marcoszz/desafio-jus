from flask import Flask
from extensions import api

from views.process import ns

app = Flask(__name__)
api.init_app(app)
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8000)