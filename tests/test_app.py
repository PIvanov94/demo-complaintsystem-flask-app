import json

from flask_testing import TestCase

from config import create_app
from db import db


class TestApplication(TestCase):
    def setUp(self) -> None:
        db.init_app(self.app)
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return create_app("config.TestApplicationConfig")

    def test_authentication_missing_auth_header_raises(self):
        url_methods = [
            ("/complainers/complaints", "GET"),
            ("/complainers/complaints", "POST"),
            ("/complainers/complaints/1", "PUT"),
            ("/complainers/complaints/1", "DELETE"),
            ("/approvers/complaints/1/approve", "PUT"),
            ("/approvers/complaints/1/reject", "PUT")
        ]
        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            else:
                resp = self.client.delete(url)

            assert resp.status_code == 400
            assert resp.json == {"message": "Invalid token"}
