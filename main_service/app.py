from main_service import create_main_app

main_app = create_main_app()

if __name__ == "__main__":
    main_app.run(port=5000)