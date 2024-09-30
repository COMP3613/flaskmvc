from .user import create_user
from .student import create_student
from .staff import create_staff
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff("Chris", "chrispass", "DCIT", "FST")
    create_staff("Shyheim", "shypass", "DCIT", "FST")
    create_student("816013453", "Matt", "Bissessar")
    create_student("816013454", "Josh", "Cabral")
    create_student("816013455", "Sayaad", "Ali")
    create_student("816013456", "Fredrick", "Chan")



