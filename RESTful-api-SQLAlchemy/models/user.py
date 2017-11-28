from db import db

# Tell SQLAlchemy this is an object we want to map by inheriting db.Model
# (Things we will be able to retrieve and send to db)

# this is an API (Not rest api), and exposes two endpoints,
# the 2 classmethods are an interface for another part of of our
# program to interact with the user (writing and retriveing from db)
# security file uses this interface to commuincate with the user in db
class UserModel(db.Model):
    # tell SQLAlchemy table name
    __tablename__ = 'users'

    # tell SQLAlchemy what columns we want the table to contain
    # id auto incremented
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # get first row (sqlAlchemy then converts it to user model object)
        return cls.query.filter_by(username=username).first()

    # id is a built in python method, so name it _id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
