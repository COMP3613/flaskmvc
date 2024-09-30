from App.database import db
from .user import User


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department = db.Column(db.String(100), nullable=True)
    faculty = db.Column(db.String(100), nullable=False)
    reports = db.relationship('Report', back_populates='staff')

    def __init__(self, username, password, department, faculty):
        super().__init__(username=username, password=password)
        self.department = department
        self.faculty = faculty

    def add_report(self, report):
        self.reports.append(report)

    def get_reports(self):
        return self.reports

    def get_reports_as_json(self):
        return [report.get_json() for report in self.reports]