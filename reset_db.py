from app import create_app, db

app = create_app()


def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset.")


if __name__ == "__main__":
    reset_db()
