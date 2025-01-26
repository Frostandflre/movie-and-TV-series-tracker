from .extensions import database

class User(database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key=True)
    nickname = database.Column(database.String(64), unique=True, index=True)
    password = database.Column(database.String(128))
    email = database.Column(database.String(120), unique=True, index=True)
    is_admin = database.Column(database.Boolean, default=False)
