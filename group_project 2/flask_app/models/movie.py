from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import review, user

class Movie:
    database = "movie_review_website"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.director = data['director']
        self.date_released = data['date_released']
        self.company = data['company']
        self.cast = data['cast']
        self.plot = data['plot']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    
    @classmethod
    def save(cls,data):
        query = "INSERT into movies (name, director, date_released, company, cast, plot, users_id) VALUES (%(name)s, %(director)s, %(date_released)s, %(company)s, %(cast)s, %(plot)s, %(users_id)s);"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE movies SET name=%(name)s, director=%(director)s, date_released=%(date_released)s, company=%(company)s, cast=%(cast)s, plot=%(plot)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(cls.database).query_db(query)
        movies = []
        for row in results:
            movies.append(cls(row))
        return movies
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM movies WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one_movie_with_user(cls,data):
        query = "SELECT * FROM movies JOIN users ON movies.users_id = users.id WHERE movies.id =%(id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            this_movie = cls(results[0])
            user_data = {
                "id": results[0]['users.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "bio": results[0]['bio'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at'],
            }
            this_user = user.User(user_data)
            this_movie.user = this_user
        return this_movie
    
    @staticmethod
    def validate_movie(movie):
        is_valid = True
        if movie['name'] == '':
            flash("Must have a name!", "movie")
            is_valid=False
        if movie['director'] == '':
            flash("Must have a director!", "movie")
            is_valid=False
        if movie['date_released'] == '':
            flash("Must have a release date!", "movie")
            is_valid=False
        if movie['company'] == '':
            flash("Must have a production company!", "movie")
            is_valid=False
        if len(movie['cast']) == '':
            flash("Must have a cast!", "movie")
            is_valid=False
        if movie['plot'] == '':
            flash("Must have a plot!", "movie")
            is_valid=False
        elif len(movie['plot']) < 15:
            flash("Plot must be at least 15 characters!", "movie")
            is_valid=False
        return is_valid