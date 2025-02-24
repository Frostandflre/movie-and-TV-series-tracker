from db_extensions import database

class MovieStatus(database.Model):
    __tablename__ = 'movie_status'
    __table_args__ = {'schema': 'movie_status_schema'}
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, nullable=False)
    movie_id = database.Column(database.String(64), nullable=False)
    movie_title = database.Column(database.String(256), nullable=True)
    status = database.Column(database.String(20), nullable=False)
    watched_date = database.Column(database.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'movie_title': self.movie_title,
            'status': self.status,
            'watched_date': self.watched_date.isoformat() if self.watched_date else None
        }
