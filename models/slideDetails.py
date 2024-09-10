from database import db

class Slide(db.Model):
    __tablename__ = 'slides'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slide_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    footer = db.Column(db.Text)
    content = db.Column(db.Text)

    # Relationship to bullet_points
    bullet_points = db.relationship('BulletPoint', back_populates='slide')

class BulletPoint(db.Model):
    __tablename__ = 'bullet_points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slide_id = db.Column(db.Integer, db.ForeignKey('slides.id'))
    level = db.Column(db.Integer)
    text = db.Column(db.Text)

    # Relationship back to slide
    slide = db.relationship('Slide', back_populates='bullet_points')
