import sys
sys.path.append("..")

from unittest import TestCase
from unittest.mock import patch

from flask import Flask
from extensions import api
from src.views import ns
from src.services.process import ProcessService  

import pytest

class TestAPI(TestCase):
    headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
    }

    url = '/processo/'

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update({
            "TESTING": True,
            "DEBUG": False
        })

        api.init_app(self.app)
        api.add_namespace(ns)

        self.client = self.app.test_client()

    def test_api_app_is_created(self):
        self.assertTrue(self.client is not None)

    def test_api_incorrect_format(self):
        # GIVEN
        data = {
            'process': '010802-55.2018.8.02.0001'
        }

        # WHEN
        response = self.client.post(
            self.url,
            json=data,
            headers=self.headers
        )

        # THEN
        self.assertEqual(response.status_code, 400)

    def test_api_invalid_court(self):
        # GIVEN
        data = {
            'process': '0710802-55.2018.8.04'
        }

        # WHEN
        response = self.client.post(
            self.url,
            json=data,
            headers=self.headers
        )

        # THEN
        self.assertEqual(response.status_code, 400)

    def test_api_invalid_segment(self):
        # GIVEN
        data = {
            'process': '0710802-55.2018.6.02.0001'
        }
       
        # WHEN
        response = self.client.post(
            self.url,
            json=data,
            headers=self.headers
        )

        # THEN
        self.assertEqual(response.status_code, 400)

    def test_api_process_not_found(self):
        # GIVEN
        data = {
            'process': '0610802-55.2018.8.02.0001'
        }
       
        # WHEN
        response = self.client.post(
            self.url,
            json=data,
            headers=self.headers
        )

        # THEN
        self.assertEqual(response.status_code, 404)

    def test_api_process_found(self):
        # GIVEN
        data = {
            'process': '0710802-55.2018.8.02.0001'
        }

        # WHEN
        response = self.client.post(
            self.url,
            json=data,
            headers=self.headers
        )

        # THEN
        self.assertEqual(response.status_code, 200)
        
