from database import db
import time

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String, db.ForeignKey('member.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = db.Column(db.BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    member = db.relationship('Member', backref=db.backref('topics', lazy=True))
    submissions = db.relationship('Submission', backref='topic', lazy='select')
