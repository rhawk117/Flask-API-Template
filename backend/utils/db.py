from flask_sqlalchemy import SQLAlchemy

# put your database utils here 

db = SQLAlchemy()

def init_db() -> None:
    from models.user import User
    from models.todo import Todo
    db.create_all()
