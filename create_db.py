from app import app, db
import os

with app.app_context():
    db.create_all()

    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
    
    print(" Database created successfully!")
    print(" DB file location:", db_path)
    