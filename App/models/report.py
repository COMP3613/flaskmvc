from datetime import datetime
from App.database import db

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    review = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', back_populates='reports')
    staff = db.relationship('Staff', back_populates='reports')

    def __init__(self, student_id, staff_id, review, rating):
        self.student_id = student_id
        self.staff_id = staff_id
        self.review = review
        self.rating = rating

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'review': self.review,
            'rating': self.rating,
            'date': self.date.isoformat()
        }