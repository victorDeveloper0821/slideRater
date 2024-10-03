from database import db

class Slide(db.Model):
    __tablename__ = 'slides'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)  
    slide_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    footer = db.Column(db.Text)
    content = db.Column(db.Text)
    
    # Relationship to submission
    submission = db.relationship('Submission', back_populates='slides', lazy='select')  # 加入關聯
    # Relationship to bullet_points
    bullet_points = db.relationship('BulletPoint', back_populates='slide', lazy='select')
