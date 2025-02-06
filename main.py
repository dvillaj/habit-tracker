from app.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    port = app.config.get("FLASK_PORT")
    host = app.config.get("FLASK_SERVER")

    app.run(host=host, port=port)