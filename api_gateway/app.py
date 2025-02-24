from api_gateway import create_gateway_app

gateway_app = create_gateway_app()

if __name__ == "__main__":
    gateway_app.run(port=5005)