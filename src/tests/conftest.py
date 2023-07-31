import sys
sys.path.append("..")

from flask import Flask
from extensions import api
from views import ns
import crawler
from services.selenium import SeleniumService

import pytest

@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    api.init_app(app)
    api.add_namespace(ns)

    return app

@pytest.fixture(scope="module")
def selenium():
    selenium = SeleniumService()
    
    return selenium