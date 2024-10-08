import os
import tempfile
import pytest
import logging
from unittest import mock

from sqlalchemy import delete
from werkzeug.security import check_password_hash, generate_password_hash
from App import *
from App.database import create_db

LOGGER = logging.getLogger(__name__)


# This fixture creates an empty database for the test and deletes it after the test
# scope="module" would execute the fixture once and reuse for all methods in the module
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


@pytest.fixture
def new_user():
    return User("bob", "bobpass")


@pytest.fixture
def hashed_password():
    return generate_password_hash("mypass", method='sha256')


def test_new_user(new_user):
    assert new_user.username == "bob"


# pure function no side effects or integrations called
def test_get_json(new_user):
    user_json = new_user.get_json()
    assert user_json == {"id": None, "username": "bob"}


def test_hashed_password(hashed_password):
    user = User("bob", "mypass")
    assert user.password != "mypass"


def test_check_password(new_user):
    assert new_user.check_password("bobpass")


def test_create_student():
    student = Student(1, "Bob", "Francis")
    assert student.student_id == 1
    assert student.firstname == "Bob"
    assert student.lastname == "Francis"


def test_create_staff():
    staff = Staff("bob", "bobpass", "DCIT", "FST")
    assert staff.username == "bob"
    assert staff.check_password("bobpass")
    assert staff.department == "DCIT"
    assert staff.faculty == "FST"


def test_create_report():
    report = Report(1, 1, "Good", 5)
    assert report.student_id == 1
    assert report.staff_id == 1
    assert report.review == "Good"
    assert report.rating == 5



