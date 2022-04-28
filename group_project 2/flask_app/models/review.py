from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import movie, user
import re
import math


class Review:
    database = "movie_review_website"
    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.movies_id = data['movies_id']
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT into reviews (rating, comment, users_id, movies_id) VALUES (%(rating)s, %(comment)s, %(users_id)s, %(movies_id)s);"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET rating=%(rating)s, comment=%(comment)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews;"
        results = connectToMySQL(cls.database).query_db(query)
        reviews = []
        for r in results:
            reviews.append(cls(r))
        return reviews
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM reviews WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_all_user(cls, data):
        query = "SELECT * FROM reviews WHERE users_id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        reviews = []
        for r in results:
            reviews.append(cls(r))
        return reviews
    
    @classmethod
    def get_all_movie(cls, data):
        query = "SELECT * FROM reviews WHERE movies_id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        reviews = []
        for r in results:
            reviews.append(cls(r))
        return reviews
    
    @classmethod
    def get_review_with_user(cls,data):
        query = "SELECT * FROM reviews JOIN users ON users.id = reviews.users_id WHERE reviews.id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        if len(results) == 0:
                return None
        else:
            review_instances = []
            for this_review_dictionary in results:
                review_instance = cls(this_review_dictionary)

            this_user_dictionary = {
                "id": this_review_dictionary['users.id'],
                "first_name": this_review_dictionary['first_name'],
                "last_name": this_review_dictionary['last_name'],
                "email": this_review_dictionary['email'],
                "password": this_review_dictionary['password'],
                "bio": this_review_dictionary['bio'],
                "created_at": this_review_dictionary['users.created_at'],
                "updated_at": this_review_dictionary['users.updated_at'],
            }
            this_user_instance = user.User(this_user_dictionary)
            review_instance.user = this_user_instance
            review_instances.append(review_instance)
        return review_instances

    
    def get_all_user(cls, data):
        query = "SELECT * FROM reviews WHERE users_id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        reviews = []
        for r in results:
            reviews.append(cls(r))
        return reviews
    
    @classmethod
    def average_score(cls, data):
        total = 0
        num = 0
        query = "SELECT rating FROM reviews WHERE movies_id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        reviews = []
        for r in results:
            reviews.append(r)
        if reviews == []:
            return "X"
        scores = []
        for x in reviews:
            scores.append(re.findall(r'\d+', str(x)))
        for n in scores:
            total = total + int(n[0])
            num = num + 1
        avg = total/num
        return round(avg, 2)

    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['comment']) < 1:
            flash("Must say something to leave a review!")
            is_valid=False
        if len(review['rating']) < 1:
            flash("Must give a score to leave a review!")
            is_valid=False
        return is_valid

    @classmethod
    def get_count_user(cls, data):
        query = "SELECT COUNT(movies_id) FROM reviews WHERE movies_id = %(id)s AND users_id = %(users_id)s;"
        movies_db = connectToMySQL(cls.database).query_db(query, data)
        string_db = str(movies_db)
        newList = list(string_db)
        newStr = ""
        for w in newList:
            if w.isdigit():
                newStr = newStr + w
        return int(newStr)