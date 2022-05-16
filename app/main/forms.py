from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Add your Bio',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Fashion blog','Fashion blog'),('Travel Blog','Travel Blog'),('Food blog','Food blog')],validators=[DataRequired()])
    description = TextAreaField('Create your blog', validators=[DataRequired()])
    submit = SubmitField('Post')
    


class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[DataRequired()])
    submit = SubmitField('Comment')