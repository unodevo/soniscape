from app import db
from werkzeug.security import generate_password_hash


# Association table for the many-to-many relationship
user_music = db.Table('user_music',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('music_id', db.Integer, db.ForeignKey('music.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    music = db.relationship('Music', secondary=user_music, backref='users')



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    song_name = db.Column(db.String(100))
    mp3_file = db.Column(db.String(200))  # Path to the mp3 file

    def __repr__(self):
        return f'<Music {self.song_name}>'