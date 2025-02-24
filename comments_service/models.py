from db_extensions import database
from _datetime import datetime

class Comments(database.Model):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'comments_schema'}
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String(256),nullable=False)
    author_nickname = database.Column(database.String(64),nullable=False)
    user_id = database.Column(database.Integer, nullable=False)
    movie_id = database.Column(database.String(64), nullable=False)
    likes = database.Column(database.Integer,default=0)
    dislikes = database.Column(database.Integer,default=0)
    publication_time = database.Column(database.DateTime, nullable=False,default=datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author_nickname': self.author_nickname,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'likes': self.likes,
            'dislikes': self.dislikes,
            'publication_time': self.publication_time.isoformat()
        }
