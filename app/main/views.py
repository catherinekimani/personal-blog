from flask import render_template,request,url_for,redirect,abort
from . import main
from ..models import User,Blog
from .forms import UpdateProfile
from .. import db,photos
from flask_login import login_required,current_user
from ..requests import get_random_quotes
from sqlalchemy import desc

@main.route('/')
def index():
    quote = get_random_quotes()
    blogs = Blog.query.all()
    user = User.query.filter_by(id=current_user.get_id()).first()
    current_post = Blog.query.order_by(desc(Blog.id)).all()
    
    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('index.html',quote = quote, blogs = blogs, user = user, current_post=current_post)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    
    if user is None:
        abort(404)
        
    return render_template('profile/profile.html', user = user)
    
    
# update profile
@main.route('/user/<name>/update', methods = ['GET', 'POST'])
def update_profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)
        
    form = UpdateProfile()
    
    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile', name = user.username))
    
    return render_template('profile/update.html',form = form)

# profile pic update
@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))