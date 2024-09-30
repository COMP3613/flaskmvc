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


def get_all_staff():
    return Staff.query.all()


def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return f"Staff member {staff_id} deleted successfully"
    return "Staff member not found"
