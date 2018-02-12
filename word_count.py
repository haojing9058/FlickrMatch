import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db
import request_api

def get_word_count(username):
    tags = db.session.query(Photo.tags).filter(Photo.username == username).all()
    tag_ls = [e for l in tags for e in l]
    word_ls = [word for sentence in tag_ls for word in sentence.split()]
    counts = Counter(word_ls)
    word_count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    word_count_df['user'] = pd.Series(username, index=word_count_df.index)
    word_count_df.columns=['word','count','user']
    return word_count_df




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

def 

def get_df(username1, username2):
    """
    """
    # Get title, description, tags of photos of username1 and username2
    df = pd.read_sql_table('photos', engine, columns=['photo_id',
            'title', 'description', 'tags', 'username'])
    df = df[df['username'].isin([username1, username2])]
    # Preprocess title, description, and tags
    df['title'] = df.title.apply(preprocess)
    df['description'] = df.description.apply(preprocess)
    df['tags'] = df.tags.apply(preprocess)


    words = pd.DataFrame(columns=['word', 'count_user1', 'count_use2', 'count_total'])

    # if word in



#convert 'tags' column as list of strings
photos['tags'] = photos.tags.apply(preprocess)


#added 100 or more photos/tags info from server
photos.merge()

