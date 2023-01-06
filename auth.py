from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .views import views
import re


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('pssword')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                return redirect(url_for('index.htnl'))
            else:
                flash("Incorrect password, try again", category='error')
        else:
            flash("Email does not exist.", category='error')
    return render_template("login.html", boolean=True)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone_no = request.form.get('phone')
        gender = request.form.get("radio")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        email_regex = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"

        if user:
            flash("user already exist!", category='error')
        elif len(password1) < 6:
            flash('Password must contains chracters greeater than 6', category='error')
        elif password1 != password2:
            flash('password don\'t match', category='error')
        elif not re.match(email_regex, email):
            flash('check and re-enter correect email..', category='error')
        elif len(fullname) == 0:
            flash('required field must be filled', category='error')
        else:
            #creating new user after succcesfl  log in
            new_user = User(name=fullname, email=email, phone_no=phone_no, gender=gender, password=generate_password_hash(password1, method='sha256' ))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html")
