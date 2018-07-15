"""For adding user and photo objects to the database"""

from model import db, User, Photo

def create_user(newuser):
    """Add user object into database."""
    if db.session.query(User).filter(User.user_id == newuser.user_id).first() is None:
        db.session.add(newuser)
        db.session.commit()

def add_photo(newphoto):
    """Add photo object into database."""
    if db.session.query(Photo).filter(Photo.photo_id == newphoto.photo_id).first() is None:
        db.session.add(newphoto)
        db.session.commit()
