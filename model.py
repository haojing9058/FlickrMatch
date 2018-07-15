"""Data modeling and database functions."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

class User(db.Model):
    """users table"""
    __tablename__ = 'users'

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id={} username={}>".format(self.user_id, self.username)

    user_id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(100), nullable=False)


class Photo(db.Model):
    """photos table"""
    __tablename__ = 'photos'

    photo_id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'))
    username = db.Column(db.String(100))
    description = db.Column(db.String())
    tags = db.Column(db.String())
    title = db.Column(db.String())
    url = db.Column(db.String(200), nullable=False)
    date_taken = db.Column(db.DateTime)
    lat = db.Column(db.String(12))
    lon = db.Column(db.String(12))
    country_code = db.Column(db.String(2))

    users = db.relationship('User', backref=db.backref('photos'))


def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use the database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flickrmatch'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."