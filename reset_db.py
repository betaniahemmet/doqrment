from app import db


def reset_db():
    db.drop_all()
    db.create_all()
    print("Database reset.")


if __name__ == "__main__":
    reset_db()
