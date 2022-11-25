from flask_app import app
from flask_app.models import user, post
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods = ['POST'])
def create_user():
    if not user.User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_in_db = user.User.get_user_by_email(data)
    if user_in_db:
        flash("*This email alredy exist, please try another one.", "emailExist")
        return redirect('/')
    user.User.create_user(data)
    return redirect('/')

@app.route('/show_user/<int:id>')
def show_user(id):
    if not session:
        return redirect('/')
    users = user.User.get_all_users()
    data = {
        'user_id': id
    }
    for x in users:
        if x['id'] == id:
            the_user = x
    posts = user.User.show_user_posts(data)
    loggedUser = user.User.get_user_by_id(session)
    return render_template('show_user.html', posts = posts, user = the_user, loggedUser = loggedUser)

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['login_email']
    }
    if not EMAIL_REGEX.match(data['email']):
        flash("*Invalid email adress.", "emailLogin")
        return redirect('/')
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("*Invalid Email/Password", "emailLogin")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        flash("*Invalid Email/Password", "emailLogin")
        return redirect('/')
    session['user_id'] = user_in_db['id']
    return redirect('/dashboard')

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')