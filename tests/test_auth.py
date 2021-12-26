import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import ComplainerModel, RoleType
from tests.helpers import object_as_dict


class TestAuth(TestCase):
    def setUp(self) -> None:
        db.init_app(self.app)
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfig")

    def test_register_complainer(self):
        url = "/register"

        data = {
            "email": "test@test.com",
            "password": "123456",
            "first_name": "Test",
            "last_name": "Testov",
            "phone": "1234567890123",
            "iban": "BG80BNBG96611020345678"
        }

        complainers = ComplainerModel.query.all()
        assert len(complainers) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201
        assert "token" in resp.json

        complainers = ComplainerModel.query.all()
        assert len(complainers) == 1
        complainer = object_as_dict(complainers[0])
        complainer.pop("password")
        data.pop("password")
        assert complainer == {"id": complainer["id"], "role": RoleType.complainer, **data}