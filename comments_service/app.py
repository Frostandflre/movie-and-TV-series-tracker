from comments_service import create_comments_app

app = create_comments_app()

if __name__ == "__main__":
    app.run(port=5003)