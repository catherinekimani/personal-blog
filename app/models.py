from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

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
    blogs = db.relationship('Blog',backref = 'blog',lazy = 'dynamic')
    comments = db.relationship('Comments',backref = 'blog',lazy = 'dynamic')
    
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
        
class Blog(db.Model):
    _tablename_='blogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(55))
    category = db.Column(db.String(255))
    description= db.Column(db.String(400))
    post_by= db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def remove_blog(self):
        db.session.delete(self)
        db.session.commit()    

    @classmethod
    def get_blogs(cls,id):
            blogs =Blog.query.filter_by(blog_id=id).all()
            return blogs  

    @classmethod
    def get_current_blog(cls,user_id):
            blogs =Blog.query.filter_by(user_id=user_id)
            return blogs      

    def repr(self):
        return f'Blog {self.description}'
    
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def remove_comment(self):
        db.session.delete(self)
        db.session.commit()    
        
    @classmethod
    def get_comments(cls,blog_id):
            comments =Comments.query.filter_by(blog_id=blog_id).all()
            return comments       
        
    def __repr__(self):
        return f'User {self.text}'