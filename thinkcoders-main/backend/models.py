from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'registration_login'

    user_id = db.Column(db.Integer, primary_key=True )
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)