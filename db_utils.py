from sqlalchemy import func
from model import connect_to_db, db, User, Photo

def create_user(newuser):
    """Add new user into database."""
    if db.session.query(User).filter(User.user_id == newuser.user_id).first() is None:
        db.session.add(newuser)
        db.session.commit()

def add_photo(newphoto):
    """Add new photo into database."""
    if db.session.query(Photo).filter(Photo.photo_id == newphoto.photo_id).first() is None:
        db.session.add(newphoto)
        db.session.commit()
