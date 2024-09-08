import time
from database import db

class Member(db.Model):
    __tablename__ = 'member'
    
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = db.Column(db.BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)
