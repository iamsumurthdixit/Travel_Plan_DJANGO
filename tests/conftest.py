import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    user = {
        "name": "test",
        "email": "test@test.com",
        "password": "test",
        "role": "user"
    }
    return user

@pytest.fixture
def admin():
    admin = {
        "name": "admintest",
        "email": "admintest@test.com",
        "password": "admintest",
        "role": "admin"
    }
    return admin

@pytest.fixture
def plan():
    with open("/Users/consultadd/tempProject copy java test/demo/planImages/sunny-weather-vector-12210439_xfAKR6i.jpg", "rb") as f:
        image_data = f.read()
    plan = {
        "title": "testplan99",
        "description": "testdesc",
        "price": 434,
        "start_date": "2023-11-11",
        "end_date": "2023-11-12",
        "image": SimpleUploadedFile("sunny-weather-vector-12210439_I8wXvnA.jpg", image_data, content_type="image/jpg"),
    }
    return plan
