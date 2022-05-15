from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @property
    def password(self):
        raise AttributeError('You cannot read the passwrd attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return f'User {self.username}'
    
# quotes class
class Quote:
    '''
    quotes class to define quotes objects
    '''
    def __init__(self,author,quote,permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink