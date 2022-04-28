from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import movie, review

class User:
    database = "movie_review_website"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movie = []

    @classmethod
    def save(cls,data):
        query = "INSERT into users (first_name, last_name, email, password, bio) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(bio)s);"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s,  password=%(password)s, bio=%(bio)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def update_bio(cls,data):
        query = "UPDATE users SET bio=%(bio)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.database).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def user_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_user(user): #cls not needed
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.database).query_db(query, user) #cls is changed to User
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken!")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords are not identical!")
            is_valid = False
        return is_valid