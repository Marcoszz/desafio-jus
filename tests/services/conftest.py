import sys
sys.path.append("..")

from flask import Flask
from extensions import api
from views import ns
import crawler

import pytest

@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "DEBUG": False
    })

    api.init_app(app)
    api.add_namespace(ns)

    yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
