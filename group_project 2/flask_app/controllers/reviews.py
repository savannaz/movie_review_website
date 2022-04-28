from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.review import Review


