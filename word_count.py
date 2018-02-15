import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db
import request_api

def get_word_count(username):
    """Return tag words and count of given user."""
    # what if user do not use tags??
    tags = db.session.query(Photo.tags).filter(Photo.username == username).all()
    #list of tuples
    tag_ls = [e for l in tags for e in l]#list of tags
    word_ls = [word for sentence in tag_ls for word in sentence.split()]#list of words
    counts = Counter(word_ls)
    word_count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    word_count_df['user'] = pd.Series(username, index=word_count_df.index)
    #sort by count and select top 30

    word_count_df.columns = ['word','count','user']
    return word_count_df

def get_csv_tags(username1, username2):
    words1 = get_word_count(username1)
    words2 = get_word_count(username2)
    common = words1.merge(words2, how='inner', on='word')
    common['count'] = common['count_x'] + common['count_y']
    common['user'] = username1+'&'+username2
    common = common[['word', 'count', 'user']]

    words1 = words1.merge(words2, how='left', on='word')
    words1 = words1[words1['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    words1.columns = ['word','count','user']

    words2 = words2.merge(words1, how='left', on='word')
    words2 = words2[words2['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    words2.columns = ['word','count','user']

    result = pd.concat([common, words1, words2])

    return result.to_csv(path_or_buth='static/tags.csv', header=False, index=False)


# df = get_word_count('chrisimmler')
# df.to_csv(path_or_buth='test.csv' columns=df.columns)
"""encoding : string, optional A string representing the encoding to use in the 
output file, defaults to ‘ascii’ on Python 2 and ‘utf-8’ on Python 3."""







# engine = create_engine('postgres:///flickrgram')

# # users = pd.read_sql_table('users', engine, columns=['user_id','username'])

# # The following done through server.py
# # #given user_id, sort, and per_page, get photos obj
# # photo_ids= request_api.get_photos_by_userid(user_id, sort, per_page)

# # #get each photo's info and add to db
# # for id in photo_ids:
# #     photo = request_api.get_photo_by_photoid(photo)
# #     db_utils.add_photo(photo)

# def preprocess (str):
#     """ Lower case and strip punctuations of a string.
#     """
#     for p in list(punctuation):
#         return str.lower().replace(p, '')


# def get_df(username1, username2):
#     """
#     """
#     # Get title, description, tags of photos of username1 and username2
#     df = pd.read_sql_table('photos', engine, columns=['photo_id',
#             'title', 'description', 'tags', 'username'])
#     df = df[df['username'].isin([username1, username2])]
#     # Preprocess title, description, and tags
#     df['title'] = df.title.apply(preprocess)
#     df['description'] = df.description.apply(preprocess)
#     df['tags'] = df.tags.apply(preprocess)


#     words = pd.DataFrame(columns=['word', 'count_user1', 'count_use2', 'count_total'])




# #convert 'tags' column as list of strings
# photos['tags'] = photos.tags.apply(preprocess)


# #added 100 or more photos/tags info from server
# photos.merge()

