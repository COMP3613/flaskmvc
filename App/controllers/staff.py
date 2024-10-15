from flask import jsonify

from App.models import staff
from App.database import db
from App.models.staff import Staff


def create_staff(username, password, department, faculty):
    newstaff = Staff(username=username, password=password, department=department, faculty=faculty)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff


def get_staff_by_id(staff_id):
    return Staff.query.filter_by(id=staff_id).first()

def get_staff_by_username(username):
    found_staff = Staff.query.filter_by(username=username).first()
    if found_staff:
        return found_staff, 200
    return jsonify("error", "Staff not found"), 404


def get_all_staff():
    return Staff.query.all(), 200

def get_all_staff_json():
    found_staff = Staff.query.all()
    if not found_staff:
        return [],404
    return [staff.get_json() for staff in found_staff], 200


def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return f"Staff member {staff_id} deleted successfully"
    return "Staff member not found"
