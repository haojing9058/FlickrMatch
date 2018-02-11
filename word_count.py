import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from model import User, Photo
from model import connect_to_db, db
import request_api



engine = create_engine('postgres:///flickrgram')

# users = pd.read_sql_table('users', engine, columns=['user_id','username'])

# The following done through server.py
# #given user_id, sort, and per_page, get photos obj
# photo_ids= request_api.get_photos_by_userid(user_id, sort, per_page)

# #get each photo's info and add to db
# for id in photo_ids:
#     photo = request_api.get_photo_by_photoid(photo)
#     db_utils.add_photo(photo)

def preprocess (str):
    """ Lower case and strip punctuations of a string.
    """
    for p in list(punctuation):
        return str.lower().replace(p, '')


#get photos df
photos = pd.read_sql_table('photos', engine, columns=['photo_id', 'user_id', 
        'title', 'description', 'tags'])[photos['user_id'].isin([user1_id, user2_id])

#convert 'tags' column as list of strings
photos['tags'] = photos.tags.apply(preprocess)


#added 100 or more photos/tags info from server
photos.merge()

