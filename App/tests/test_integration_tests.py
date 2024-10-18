import pytest
import logging
from werkzeug.security import generate_password_hash
from App import create_app, db, login
from App.database import create_db
from App.models import User, Student, Staff, Report

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@pytest.fixture(scope="function")
def test_client():
    """Create a new app instance for testing per test function."""
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()


def test_create_user(test_client):
    user = User(username="bob", password="bobpass")
    db.session.add(user)
    db.session.commit()

    # Check if user is created in the database
    user_in_db = db.session.query(User).filter_by(username="bob").first()
    assert user_in_db is not None
    assert user == user_in_db


def test_authenticate(test_client):
    user = User(username="bob", password="bobpass")
    db.session.add(user)
    db.session.commit()

    assert login("bob", "bobpass") is not None


def test_get_all_users_json(test_client):
    user1 = User(username="bob", password="bobpass")
    user2 = User(username="rick", password="rickpass")
    db.session.add_all([user1, user2])
    db.session.commit()

    users = User.query.all()
    users_json = [{"id": user.id, "username": user.username} for user in users]
    assert users_json == [{"id": user1.id, "username": "bob"}, {"id": user2.id, "username": "rick"}]


def test_create_student(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    db.session.add(student)
    db.session.commit()

    student_in_db = db.session.query(Student).filter_by(student_id=1).first()
    assert student_in_db is not None
    assert student_in_db.firstname == "Bob"


def test_create_report(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    staff = Staff(username="bob", password="bobpass", department="DCIT", faculty="FST")
    db.session.add_all([student, staff])
    db.session.commit()

    report = Report(student_id=student.student_id, staff_id=staff.id, review="Good", rating=5)
    db.session.add(report)
    db.session.commit()

    report_in_db = db.session.query(Report).filter_by(student_id=student.student_id).first()
    assert report_in_db is not None
    assert report_in_db.review == "Good"
    assert report_in_db.rating == 5


def test_get_student_reports(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    staff = Staff(username="bob", password="bobpass", department="DCIT", faculty="FST")
    db.session.add_all([student, staff])
    db.session.commit()

    report = Report(student_id=student.student_id, staff_id=staff.id, review="Excellent", rating=4)
    db.session.add(report)
    db.session.commit()

    reports = db.session.query(Report).filter_by(student_id=student.student_id).all()
    assert len(reports) == 1
    assert reports[0].review == "Excellent"


def test_update_user(test_client):
    user = User(username="bob", password="bobpass")
    db.session.add(user)
    db.session.commit()

    user_to_update = db.session.query(User).filter_by(username="bob").first()
    user_to_update.username = "ronnie"
    db.session.commit()

    updated_user = db.session.query(User).filter_by(username="ronnie").first()
    assert updated_user is not None
    assert updated_user.username == "ronnie"


def test_update_report(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    staff = Staff(username="bob", password="bobpass", department="DCIT", faculty="FST")
    db.session.add_all([student, staff])
    db.session.commit()

    report = Report(student_id=student.student_id, staff_id=staff.id, review="Good", rating=5)
    db.session.add(report)
    db.session.commit()

    report_to_update = db.session.query(Report).filter_by(student_id=student.student_id).first()
    report_to_update.review = "Excellent"
    report_to_update.rating = 4
    db.session.commit()

    updated_report = db.session.query(Report).filter_by(student_id=student.student_id).first()
    assert updated_report.review == "Excellent"
    assert updated_report.rating == 4


def test_delete_student(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    db.session.add(student)
    db.session.commit()

    student_to_delete = db.session.query(Student).filter_by(student_id=1).first()
    db.session.delete(student_to_delete)
    db.session.commit()

    deleted_student = db.session.query(Student).filter_by(student_id=1).first()
    assert deleted_student is None


def test_delete_report(test_client):
    student = Student(student_id=1, firstname="Bob", lastname="Francis")
    staff = Staff(username="bob", password="bobpass", department="DCIT", faculty="FST")
    db.session.add_all([student, staff])
    db.session.commit()

    report = Report(student_id=student.student_id, staff_id=staff.id, review="Good", rating=5)
    db.session.add(report)
    db.session.commit()

    report_to_delete = db.session.query(Report).filter_by(student_id=student.student_id).first()
    db.session.delete(report_to_delete)
    db.session.commit()

    deleted_report = db.session.query(Report).filter_by(student_id=student.student_id).first()
    assert deleted_report is None
