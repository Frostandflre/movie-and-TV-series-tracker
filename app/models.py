from .extensions import database

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
    status = database.Column(database.String(20), nullable=False)
