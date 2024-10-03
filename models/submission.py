from database import db
import time

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    filename = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = db.Column(db.BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)
    status = db.Column(db.Integer)

    # Relation to Topic
    topic = db.relationship('Topic', back_populates='submissions', lazy='select')
    # Relationship to slides
    slides = db.relationship('Slide', back_populates='submission', lazy='select')  # 添加反向關聯