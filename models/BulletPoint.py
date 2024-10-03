from database import db

class BulletPoint(db.Model):
    __tablename__ = 'bullet_points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slide_id = db.Column(db.Integer, db.ForeignKey('slides.id'))
    level = db.Column(db.Integer)
    text = db.Column(db.Text)

    # Relationship back to slide
    slide = db.relationship('Slide', back_populates='bullet_points', lazy='select')
