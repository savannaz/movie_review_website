from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.movie import Movie
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=["POST"])
def create():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "bio" : request.form['bio']
    }
    id = User.save(data)
    session['users_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    user = User.user_email(request.form)
    if not user:
        flash("Invalid email!")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password!")
        return redirect('/')
    session['users_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['users_id']
    }
    return render_template("dashboard.html", user = User.user_id(data), movies = Movie.get_all(), reviews = Review.get_all(), users = User.get_all())

@app.route('/user/edit/<int:id>')
def edit_user(id):
    if 'users_id' not in session:
        return redirect('/logout')
    user_data = {"id":id}
    return render_template('edit_user.html', user = User.user_id(user_data), users = User.get_all())

@app.route('/user/update', methods=["POST"])
def update_user():
    if 'users_id' not in session:
        return redirect('/logout')
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "bio" : request.form['bio']
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/user/update_bio/<int:id>', methods=["POST"])
def update_bio(id):
    if 'users_id' not in session:
        return redirect('/logout')
    
    data = {
        "bio": request.form['bio'],
        "id": id
    }
    User.update_bio(data)
    return redirect(f"/user/{id}")

@app.route('/user/<int:id>')
def show_user(id):
    if 'users_id' not in session:
        return redirect('/logout')
    user_data={
        "id":id
    }
    data={'id': session['users_id']}
    return render_template('user.html', user = User.user_id(data), userVis = User.user_id(user_data), users = User.get_all(), movies = Movie.get_all(), reviews = Review.get_all())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')