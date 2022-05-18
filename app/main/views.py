from curses import flash
from flask import render_template,request,url_for,redirect,abort
from . import main
from ..models import User,Blog,Comments,Subscriber
from .forms import UpdateProfile,BlogForm,CommentForm
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

# comments
@main.route('/comments/<int:blog_id>', methods=['GET','POST'])
@login_required
def new_comments(blog_id):
    comments = Comments.get_comments(blog_id)
    blog = Blog.query.get(blog_id)
    post_by = Blog.user_id
    user = User.query.filter_by(id=post_by).first()
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data      
        new_comment = Comments(text=comment, blog_id=blog_id, user_id=current_user.get_id())
        new_comment.save_comment()
        return redirect(url_for('main.index',blog_id = blog_id))

    return render_template('comments.html',Commentsform=form, comments=comments, blog = blog, user=user)

# new blog
@main.route('/new_blog', methods=['POST','GET'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        post_by = form.post_by.data
        user_id = current_user
        new_blog =Blog(description=description,user_id=current_user._get_current_object().id,category=category,title=title,post_by=post_by)
        new_blog.save_blog()
        return redirect(url_for('main.index'))
    return render_template('new_blog.html', form = form)

# delete blog
@main.route('/delete_blog/<int:id>',methods = ['GET','POST'])
@login_required
def delete(id):
    blog= Blog.query.get(id)
    blog.remove_blog()
    return redirect(url_for('main.index'))

# delete comment
@main.route('/delete_comment/<int:id>',methods = ['GET','POST'] )
@login_required
def delete_comment(id):
    comments = Comments.query.filter_by(id=id).first()
    comments.remove_comment()
    return redirect(url_for('main.index'))

# subscription
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
        """
        subscribe function that subscribes the user to the post
        """
        email = request.args.get('email')
        new_subscriber = Subscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        return redirect(url_for('main.index'))

# edit blog
@main.route('/blog/<blog_id>/edit',methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog=Blog.query.filter_by(id=blog_id).first()
    if blog.post_by.id !=current_user.id:
        abort(403)

    form=BlogForm()
    if form.validate_on_submit():
        blog.title=form.title.data
        blog.description=form.description.data
        db.session.commit()
        return redirect(url_for('.blog',blog_id=blog.id) )
    elif request.method=='GET':
        form.title.data=blog.title
        form.description.data=blog.description
        

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