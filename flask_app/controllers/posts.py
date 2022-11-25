from flask_app import app
from flask_app.models import user, post
from flask import render_template, redirect, request, session, flash

@app.route('/dashboard')
def dashboard():
    if not session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = user.User.get_user_by_id(data)
    posts = post.Post.get_all_posts(data)
    user_liked_posts = user.User.get_user_logged_liked_posts(data)
    all_users = user.User.get_all_users()
    return render_template('dashboard.html', loggedUser = loggedUser, posts = posts, user_liked_posts = user_liked_posts, all_users = all_users)

@app.route('/create_post', methods = ['POST'] )
def create_post():
    if not post.Post.validate_post(request.form):
        return redirect(request.referrer)
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    post.Post.create_post(data)
    return redirect(request.referrer)

@app.route('/like/<int:post_id>')
def add_like(post_id):
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    post.Post.add_like(data)
    return redirect('/dashboard')

@app.route('/unlike/<int:post_id>')
def remove_like(post_id):
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    post.Post.remove_like(data)
    return redirect('/dashboard')

@app.route('/delete_post/<int:post_id>')
def remove_post(post_id):
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    post.Post.remove_post(data)
    return redirect('/dashboard')

@app.route('/edit_post/<int:id>')
def edit_user(id):
    if not session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = user.User.get_user_by_id(data)
    results = post.Post.get_all_posts(data)
    for row in results:
        if row['id']== id:
            the_post = row
    return render_template('edit.html', post = the_post, loggedUser = loggedUser)

@app.route('/update/<int:id>', methods = ['POST'])
def update_user(id):
    if not session:
        return redirect('/')
    data = {
        'post_id': id,
        'user_id': session['user_id'],
        'content': request.form['content']
    }
    post.Post.update_post(data)
    return redirect('/dashboard')