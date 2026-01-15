from config import db, app
from models import Episode, Guest, Appearance

# Script to manually create database tables if migrations are not used
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")