from app import create_backend_app

def main():
    app = create_backend_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
