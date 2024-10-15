from flask import jsonify

from App.models import Report, Student, Staff
from App.database import db


def get_all_reports(order):
    if order == 'asc':
        return Report.query.order_by(Report.rating).all(), 200
    return Report.query.order_by(Report.rating.desc()).all(), 200


def get_all_reports_json():
    reports = Report.query.order_by(Report.date).all()
    reports_collection = [report.get_json() for report in reports]
    return jsonify(reports_collection), 200


def create_report(student_id, staff_id, review, rating):
    student = Student.query.filter_by(student_id=student_id).first()
    staff = Staff.query.get(staff_id)
    print(student)
    print(staff)
    if not student or not staff:
        return "Student or staff member not found."

    if not 1 <= rating <= 5:
        return "Invalid rating. Rating must be between 1 and 5."

    new_report = Report(
        student_id=student.id,
        staff_id=staff.id,
        review=review,
        rating=rating
    )

    db.session.add(new_report)
    db.session.commit()

    return f"Report created for {student.firstname} {student.lastname} by {staff.username}: {review} with rating {rating}"


def get_student_reports(student_id):
    student = Student.query.get(student_id)
    if student:
        return student.reports
    return []


def update_report(report_id, review, rating, new_student_id=None):
    report = Report.query.get(report_id)
    if not report:
        return "Report not found."
    rating = int(rating)
    if not (1 <= rating <= 5):
        return "Invalid rating. Rating must be between 1 and 5."
    old_student_id = report.student_id
    report.review = review
    report.rating = rating
    if new_student_id:
        student = Student.query.filter_by(student_id=new_student_id).first()
        if student:
            report.student_id = student.id
            old_student = Student.query.get(old_student_id)
            if old_student and report_id in old_student.reports:
                old_student.reports.remove(report)
                db.session.commit()
        else:
            return "Student not found."
    db.session.commit()
    return f"Report {report_id} updated successfully."


def delete_report(report_id):
    report = Report.query.get(report_id)
    if not report:
        return "Report not found."
    db.session.delete(report)
    db.session.commit()
    return f"Report {report_id} deleted successfully."
