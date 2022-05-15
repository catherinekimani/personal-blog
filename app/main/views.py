from flask import render_template,request,url_for,redirect,abort
from . import main
from ..models import User

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('index.html')

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = user).first()
    
    if user is None:
        abort(404)
        
    return render_template('profile/profile.html', user = user)
    
    