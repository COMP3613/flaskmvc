from App import Report
from App.models import Student
from App.database import db
from datetime import datetime


def create_student(student_id, firstname, lastname):
    existing_student = Student.query.filter_by(student_id=student_id).first()
    if existing_student:
        return "Student with this ID already exists"

    new_student = Student(student_id=student_id, firstname=firstname, lastname=lastname)
    db.session.add(new_student)
    db.session.commit()
    return new_student


def get_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        return student
    return "Student not found"


def get_all_students():
    return Student.query.all()


def get_student_by_id(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        print("THIS IS STUDENT!!!!")
        print(student)
        return student
    return "No student found"


def get_student_by_name(firstname, lastname):
    student = Student.query.filter_by(firstname=firstname, lastname=lastname).first()
    if student:
        return student
    return "No student found"


def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    return [student.get_json() for student in students]


def update_student(student_id, firstname=None, lastname=None, updatedid=None):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return "Student not found"

    if firstname:
        student.firstname = firstname

    if lastname:
        student.lastname = lastname

    if updatedid:
        student.student_id = updatedid

    db.session.commit()
    return student


def delete_student(student_id):
    # print(f"call made to delete: {student_id}")
    student = Student.query.filter_by(student_id=student_id).first()
    # print(f"student is: student")
    if student:
        for report in student.reports:
            db.session.delete(report)
        db.session.delete(student)
        db.session.commit()
        return f"Student {student_id} deleted successfully"

    return "Student not found"


# def add_report_to_student(student_id, report, rating):
#     student = Student.query.filter_by(student_id=student_id).first()
#     if not student:
#         return "Student not found"
#
#     if not (1 <= rating <= 5):
#         return "Rating must be between 1 and 5"
#
#     new_report = Report(student_id=student.id, report=report, rating=rating, date=datetime.now())
#
#     db.session.add(new_report)
#     db.session.commit()
#     return new_report
#

def get_student_reports(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return "Student not found"

    return student.reports


def get_student_as_json(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        return student.get_json()
    return "Student not found"
