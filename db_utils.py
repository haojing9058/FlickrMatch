from sqlalchemy import func
from model import connect_to_db, db, User, Photo
# import request_api
# from server import app
# from datetime import datetime

def create_user(newuser):

    if db.session.query(User).filter(User.user_id == newuser.user_id).first() is None:
        db.session.add(newuser)
        db.session.commit()

def add_photo():
    pass


