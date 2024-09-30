from App.database import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    reports = db.relationship('Report', back_populates='student', lazy=True)

    def __init__(self, student_id, firstname, lastname):
        self.student_id = student_id
        self.firstname = firstname
        self.lastname = lastname

    def add_report(self, report):
        self.reports.append(report)

    def get_reports(self):
        return self.reports

    def get_reports_as_json(self):
        return [report.get_json() for report in self.reports]

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'report_count': len(self.reports)
        }
