"""
This file will hold all the database related methods required for the flask app. 
Additonally, if this file is run, then app context will be acheived which is helpful
for developmental purposes.
"""
import hashlib
import flask_sqlalchemy
import uuid
import os
import server
import helpers

CHARACTER_LIMIT = 80

db = flask_sqlalchemy.SQLAlchemy()


class User( db.Model ):
    id = db.Column( db.String(32), primary_key=True )
    #user config
    username = db.Column( db.String(CHARACTER_LIMIT), unique=True, nullable=False )
    email = db.Column( db.String(100), unique=True, nullable=False )
    password = db.Column( db.String(64), nullable=False )
    #user status
    balance = db.Column( db.Float )

    def __init__(self, username: str, email: str, password: str):
        self.id = str(uuid.uuid4())
        
        self.username = username
        self.email = email
        self.password = hashlib.sha256( password.encode() ).hexdigest() #hash the password for security

        self.balance = 0

    def deposit(self, amount: float):
        if type(amount) != float and type(amount) != int :
             raise("Invalid amount!")
        self.balance += amount

    def valid_password(self, password: str):
        return self.password == hashlib.sha256(password.encode()).hexdigest()


def get_username( username: str ) -> User:
    """
    checks whether username exists, and if it does then return that user
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise("Username does not exist!")
    else:
        return user


def create_user( username: str, email: str, password: str):
    """
    create an account given a username and an email
    """
    if not helpers.valid_email( email ):
        raise("Invalid Email!")
    if len(username) > CHARACTER_LIMIT:
        raise("Username or Email is too long!")
    new_user = User( username, email, password )
    try:
        db.session.add( new_user )
        db.session.commit()
    except:
        raise("Email or Username not unique!")

#have this return a token if true, so the browswer can store it
def authenticate_user( username: str, password: str ) -> bool:
    """
    confirms whether or not username and password are a matching pair
    """
    current_user = get_username( username )
    return current_user.valid_password( password )


def deposit( username: str, amount: float ):
    """
    given a username, deposit amount money into their account
    """
    current_user = get_username(username)
    current_user.deposit( amount )
    db.session.commit()





#DEVELOPMENTAL SECTION
def reset_database():
    """
    Delete the old database and create a new one
    """
    try:
        os.system("rm database.sqlite")
    except:
        pass
    #create new one
    with server.create_app().app_context():
        db.create_all()

def app_context():
    """
    Push app context so database operations can be run on IDLE.
    """
    app = server.create_app()
    app.app_context().push()
