"""Models and database function for Flickrgram project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of the website"""
    __tablename__ = 'users'

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id={} username={} realname{} user_location={} photo_count={}> photo_since={} profile_url={}"
        .format(self.user_id, self.username, self.realname, self.user_location
        self.photo_count, self.photo_since, self.profile_url)

    user_id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    realname = db.Column(db.String(50))
    user_location = db.Column(db.String(50))
    photo_count = db.Column(db.Integer, nullable=False)
    photo_since = db.Column(db.Datetime)
    profile_url = db.Column(db.String(200), nullable=False)


class Photo(db.Model):
    """Photo in the website """
    __tablename__ = 'photos'

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Photo photo_id={} user_id={} title{} tags={} description={} date_posted={} date_taken={} country={} place_id={} lat={} lon={}>"
        .format(self.photo_id, self.user_id, self.title, self.tags, self.description,
            self.date_posted, self.date_taken, self.country, self.place_id,
            self.lat, self.lon)

    photo_id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'))
    title = db.Column(db.String(100))
    tags = db.Column(db.String())
    description = db.Column(db.String())
    date_posted = dbColumn(db.Datetime, nullable=False)
    date_taten = db.Column(db.Datetime)
    country = db.Column(db.String(20))
    place_id = db.Column(db.String(30))
    lat = db.Column(db.String(15))
    lon = db.Column(db.String(15))

    users = db.relationship('User', backref=db.backref('photos'))


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flickrgram'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

