from config import Config
from tmdbv3api import TMDb,Movie

tmdb = TMDb()
tmdb.api_key = Config.TMDb_API
tmdb.language = 'ru'

def get_movie_info(movie_id): #TODO: что то сделать с тем что TMDb отдаёт мне информацию о фильме на всех языках
    movie = Movie()
    movie_info = movie.details(movie_id)
    if not movie_info:
        return None
    return movie_info

def get_popular_movies():
    movie = Movie()
    return movie.popular()

if __name__ == "__main__":
    print(get_movie_info(550))