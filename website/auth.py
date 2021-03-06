import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta, datetime, time


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if 'signup' in request.form:
        return redirect(url_for('auth.signup'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.homePage'))

            else:
                flash('Incorrect password, try again.')
        else:
            flash('Email does not exist.')

    return render_template("index.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You successfully logout.')
    return redirect(url_for('auth.login'))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    session.pop('_flashes', None)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confPassword = request.form.get('passwordconfirm')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.')
        elif password != confPassword:
            flash('Passwords don\'t match.')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            login_user(new_user, remember=True)
            return redirect(url_for('views.homePage'))

    return render_template("signup.html", user=current_user)
