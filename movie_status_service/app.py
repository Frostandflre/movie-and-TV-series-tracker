from movie_status_service import create_movie_status_app

app = create_movie_status_app()

if __name__ == "__main__":
    app.run(port=5002)