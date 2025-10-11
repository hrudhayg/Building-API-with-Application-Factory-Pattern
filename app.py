from application import create_app

app = create_app()

if __name__ == "__main__":
    # Use reloader only in dev
    app.run(debug=True)
