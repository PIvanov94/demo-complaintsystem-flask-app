import json
import os.path
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from managers.complaint import ComplaintManager
from models import ComplaintModel, State
from services.s3 import S3Service
from tests.factories import ComplainerFactory
from tests.helpers import encoded_photo, generate_token, object_as_dict, mock_uuid


class TestComplaint(TestCase):
    def setUp(self) -> None:
        db.init_app(self.app)
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfig")

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(ComplaintManager, "issue_transaction", return_value=None)
    @patch.object(S3Service, "upload_photo", return_value="some-test.url")
    def test_create_complaint(self, s3_mock, wise_mock):
        url = "/complainers/complaints"
        data = {
            "title": "Test title",
            "description": "Test description",
            "photo": encoded_photo,
            "photo_extension": "jpg",
            "amount": 10.69
        }
        complainer = ComplainerFactory()
        token = generate_token(complainer)
        self.headers.update({"Authorization": f"Bearer {token}"})
        complaints = ComplaintModel.query.all()
        assert len(complaints) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        complaints = ComplaintModel.query.all()
        assert len(complaints) == 1

        data.pop("photo")
        extension = data.pop("photo_extension")
        created_complaint = object_as_dict(complaints[0])
        created_complaint.pop("create_on")
        assert created_complaint == {
            "id": complaints[0].id,
            "photo_url": "some-test.url",
            "status": State.pending,
            "complainer_id": complainer.id,
            **data
        }

        expected_resp = {
            "id": complaints[0].id,
            "photo_url": "some-test.url",
            "status": State.pending.value,
            **data
        }
        actual_resp = resp.json
        actual_resp.pop("create_on")
        assert resp.status_code == 201
        assert actual_resp == expected_resp

        photo_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)
        s3_mock.assert_called_once_with(path, photo_name)

        wise_mock.assert_called_once_with(data["amount"],
                                          f"{complainer.first_name} "
                                          f"{complainer.last_name}",
                                          complainer.iban,
                                          complaints[0].id
                                          )
