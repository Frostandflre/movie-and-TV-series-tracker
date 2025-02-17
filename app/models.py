from .extensions import database
from datetime import datetime

class Users(database.Model):
    user_id = database.Column(database.Integer,primary_key=True)
    nickname = database.Column(database.String(64), unique=True, index=True)
    password = database.Column(database.String(512))
    email = database.Column(database.String(120), unique=True, index=True)
    is_admin = database.Column(database.Boolean, default=False)

class MovieStatus(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey("users.user_id"), nullable=False)
    movie_id = database.Column(database.String(64), nullable=False)
    movie_title = database.Column(database.String(256), nullable=True)
    status = database.Column(database.String(20), nullable=False)
    watched_date = database.Column(database.DateTime, nullable=True)

class Comments(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String(256),nullable=False)
    author_nickname = database.Column(database.String(64), database.ForeignKey("users.nickname"),nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey("users.user_id"), nullable=False)
    movie_id = database.Column(database.String(64), nullable=False)
    likes = database.Column(database.Integer,default=0)
    dislikes = database.Column(database.Integer,default=0)
    publication_time = database.Column(database.DateTime, nullable=False,default=datetime.now())
