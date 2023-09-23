from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
import random
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from django import forms
from forms import CreatePostForm
from flask_gravatar import Gravatar
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf import FlaskForm
from functools import wraps
from flask_ckeditor import CKEditorField

app = Flask(__name__)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CreateCustomer(UserMixin, db.Model):
    __tablename__ = "new_users"
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(250), nullable=False, unique=True)
    Name = db.Column(db.String(250), nullable=False)
    Phone = db.Column(db.Integer(), nullable=False)
    Password = db.Column(db.String(250), nullable=False)
    start_point = db.Column(db.String(250), nullable=False)
    end_point = db.Column(db.String(250), nullable=False)
    child_one = relationship('Items', back_populates='father')


db.create_all()

class Shops(UserMixin, db.Model):
    __tablename__ = 'shop_owners'
    id = db.Column(db.Integer, primary_key=True)
    # Email = db.Column(db.String(250), nullable=False, unique=True)
    Shop_name = db.Column(db.String(250), nullable=False, unique=True)
    Password = db.Column(db.String(250), nullable=False)
    child_two = relationship("Items", back_populates="father")
    stepfather = relationship("UserComments", back_populates="child_two")


db.create_all()

class Items(UserMixin, db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(250), nullable=False, unique=True)
    restaurant = Column(String(250), ForeignKey('shop_owners.Shop_name'))
    item_cost = db.Column(db.String(250), nullable=False)
    father = relationship('Shops', back_populates='child_two')

db.create_all()

class CustItems(UserMixin, db.Model):
    __tablename__ = 'customer_items'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = Column(String(250), ForeignKey('new_users.Name'))
    otp = Column(db.Integer, nullable=False )    # will set otp during creation of cust item db using random module

db.create_all()


class RegisterForm(FlaskForm):
    email = StringField('Enter Email ID', validators=[InputRequired()])
    password = StringField('Enter password', validators=[InputRequired()])
    user = StringField('Enter an username', validators=[InputRequired()])
    submit = SubmitField('Register!')

class LogInForm(FlaskForm):
    Email = StringField('User ID', validators=[InputRequired()])
    Password = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


# @app.route("/")
# def hello():
#     return render_template("index.html")
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if request.method == 'POST':
#         new_user = CreateCustomer(Email=request.form.get('Email'), Name=request.form.get('Name'),
#                                Password=generate_password_hash(request.form.get('Password'), method='pbkdf2:sha256',
#                                                                salt_length=8), start_pt=request.form.get('Start'),
#                                   end_pt=request.form.get('End'))
#         if CreateCustomer.query.filter_by(Email=request.form.get('Email')).first():
#             flash('this email is already registered!')
#             return redirect(url_for('login'))
#         else:
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user)
#             return redirect(url_for('/main'))
#     return render_template("register.html", form=form, logged_in=current_user.is_authenticated)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login = LogInForm()
#     if request.method == 'POST':
#         user = CreateCustomer.query.filter_by(Email=login.Email.data).first()
#         user_log_psw = login.Password.data
#         if user is not None:
#             if check_password_hash(user.Password, user_log_psw):
#                 login_user(user)
#                 return redirect(url_for('get_all_posts'))
#             else:
#                 flash('password is incorrect!')
#                 return redirect(url_for('login'))
#         else:
#             flash('user not registered!')
#             # if user.id == 1:
#             #     posts = BlogPost.query.all()
#             #     return render_template('index.html', logged_in=current_user.is_authenticated, all_posts=posts)
#             # else:
#             #     return redirect(url_for('get_all_posts'))
#     return render_template("login.html", form=login, logged_in=current_user.is_authenticated)
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('/'))
#
#
#
# if __name__=="__main__":
#     app.run(debug=True)



