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

def get_popular_movies(page = 1):
    movie = Movie()
    return movie.popular(page=page)

def search_movie(term,page = 1):
    movie = Movie()
    return movie.search(term,page = page)

if __name__ == "__main__":
    print(search_movie("Interception"))
