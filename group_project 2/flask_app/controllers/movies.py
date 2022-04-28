from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app
from flask_app.controllers.users import dashboard
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.review import Review

@app.route('/movie/new')
def new_movie():
    data = {
        'id': session['users_id']
    }
    return render_template('new.html', user = User.user_id(data))

@app.route('/movie/create', methods=['POST'])
def create_movie():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Movie.validate_movie(request.form):
        return redirect('/movie/new')
    data = {
        "name": request.form["name"],
        "director": request.form["director"],
        "date_released": request.form["date_released"],
        "company": request.form["company"],
        "cast": request.form["cast"],
        "plot": request.form["plot"],
        "users_id": session["users_id"]
    }
    Movie.save(data)
    return redirect('/dashboard')

@app.route('/movie/edit/<int:id>')
def edit_movie(id):
    data = {"id":id}
    user_data = {"id":session['users_id']}
    return render_template('edit_movie.html', movie = Movie.get_one(data), user = User.user_id(user_data), users = User.get_all())

@app.route('/movie/update/<int:id>', methods=['POST'])
def update_movie(id):
    if 'users_id' not in session:
        return redirect('/logout')
    if not Movie.validate_movie(request.form):
        return redirect(request.referrer)
    data = {
        "name": request.form["name"],
        "director": request.form["director"],
        "date_released": request.form["date_released"],
        "company": request.form["company"],
        "cast": request.form["cast"],
        "plot": request.form["plot"],
        "id": id
    }
    Movie.update(data)
    return redirect('/dashboard')

@app.route('/movie/<int:id>')
def show_movie(id):
    data = {"id":id,
            "users_id": session['users_id']}
    user_data = {"id":session['users_id']}
    return render_template('movie.html', movie = Movie.get_one_movie_with_user(data), user = User.user_id(user_data), users = User.get_all(), reviews = Review.get_all_movie(data), average_score = Review.average_score(data), userCount = Review.get_count_user(data))

@app.route('/create/review/<int:id>', methods=["POST"])
def create_review(id):
    user_data = {"id":session['users_id']}
    if not Review.validate_review(request.form):
        return redirect(f"/movie/{id}")
    data = {
        "rating": request.form['rating'],
        "comment": request.form['comment'],
        "users_id": session['users_id'],
        "movies_id": id
    }
    Review.save(data)
    return redirect(f"/movie/{id}")

@app.route('/review/delete/<int:id>')
def destroy_review(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {"id":id}
    Review.destroy(data)
    return redirect('/dashboard')

@app.route('/review/edit/<int:id>')
def edit_review(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {"id":id}
    user_data = {"id":session['users_id']}
    return render_template('edit_review.html', review = Review.get_one(data), user = User.user_id(user_data))

@app.route('/review/update/<int:id>', methods=["POST"])
def update_review(id):
    if 'users_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect(request.referrer)
    data = {
        "rating" : request.form['rating'],
        "comment" : request.form['comment'],
        "id" : id
    }
    Review.update(data)
    return redirect('/dashboard')

