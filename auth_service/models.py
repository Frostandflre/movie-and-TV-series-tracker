from db_extensions import database

class Users(database.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'users_schema'}
    user_id = database.Column(database.Integer,primary_key=True)
    nickname = database.Column(database.String(64), unique=True, index=True)
    password = database.Column(database.String(512))
    email = database.Column(database.String(120), unique=True, index=True)
    is_admin = database.Column(database.Boolean, default=False)