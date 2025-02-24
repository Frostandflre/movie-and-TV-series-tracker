from auth_service import create_auth_app

app = create_auth_app()

if __name__ == "__main__":
    app.run(port=5001)