from datetime import datetime
from database import db

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String, db.ForeignKey('member.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    member = db.relationship('Member', backref=db.backref('topics', lazy=True))
    submissions = db.relationship('Submission', backref='topic', lazy='select')
