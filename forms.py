from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, InputRequired
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    username = StringField("User ID", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    # img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    # body = CKEditorField("Blog Content", validators=[DataRequired()])
    start = StringField("Enter start location", validators=[InputRequired()])
    end = StringField("Enter ending location", validators=[InputRequired()])
    submit = SubmitField("Submit Post")