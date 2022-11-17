from . import db
import enum

class Status(enum.Enum):
    reading = 1 
    finished = 2 
    waiting = 3 
    skimmed = 4
    dnf = 5


class Students(db.Model): # type: ignore
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)


class Books(db.Model): # type: ignore
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    name = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable = False)
    pages = db.Column(db.Integer, nullable = True)
    bookcover = db.Column(db.String(), nullable = False)
    status = db.Column(db.Enum(Status))
    currentpage = db.Column(db.Integer(), nullable = True)


class Challenges(db.Model): # type: ignore
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    badge = db.Column(db.String(), nullable = False)

class Goals(db.Model): # type: ignore
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    goal = db.Column(db.String())
    checked = db.Column(db.Boolean)