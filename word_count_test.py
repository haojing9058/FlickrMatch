import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db


def get_tags_df(username1, username2, text_type='tags'):
    """Return certain text_type of word counts for each user and their common word counts"""
    def get_word_count(username, text_type):
        """Return certain text_type of word counts dataframe for a given user.
        (string1, string2) --> dataframe
        text_type: options of "tags", title", "description". Defalt to "tags".
        """
        #get a list of tutples of srtings
        if text_type == 'tag':
            raw_data = db.session.query(Photo.tags).filter(Photo.username == username).all()
        elif text_type == 'title':
            raw_data = db.session.query(Photo.title).filter(Photo.username == username).all()
        elif text_type == 'description':
            raw_data = db.session.query(Photo.description).filter(Photo.username == username).all()
        # what if user do not use tags??
        #get a list of strings
        record_ls = [e for l in raw_data for e in l]
        #get a list of words
        word_ls = [word for sentence in record_ls for word in sentence.split()]
        #get word count dictionary
        counts = Counter(word_ls)
        #convert dict to dataframe
        word_count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        #add "user" column to the dataframe
        word_count_df['user'] = pd.Series(username, index=word_count_df.index)
        #rename columns
        word_count_df.rename(columns={'index':'word', 0:'count', 'user':'user'}, inplace=True)
        #sort and select top 20
        df = word_count_df.sort_values(by='count',ascending = False).head(20)

        return df

    #word counts for each user
    words1 = get_word_count(username1, text_type)
    words2 = get_word_count(username2, text_type)

    #common word and sum of counts
    common = words1.merge(words2, how='inner', on='word')
    common['count'] = common['count_x'] + common['count_y']
    common['user'] = 'common'
    common = common[['word', 'count', 'user']]

    #word counts by user 1 only
    words1 = words1.merge(words2, how='left', on='word')
    words1 = words1[words1['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    words1.columns = ['word','count','user']

    #word counts by user 2 only
    words2 = words2.merge(common, how='left', on='word')
    words2 = words2[words2['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    words2.columns = ['word','count','user']

    #concatenat the common, user 1 only, and user 2 only
    df = pd.concat([common, words1, words2])

    return df

def get_tags_csv(df):
    """Save tags dataframe to .csv"""
    return df.to_csv(path_or_buf=r'static/tags.csv', header=False, index=False)

def get_title_csv(df):
    """Save title dataframe to .csv"""
    return df.to_csv(path_or_buf=r'static/title.csv', header=False, index=False)

def get_description_csv(df):
    """Save title dataframe to .csv"""
    return df.to_csv(path_or_buf=r'static/description.csv', header=False, index=False)

def get_match_score(df):
    """ Calculate match score given the "word, count, user" df.
    """
    sum_of_common = df.loc[df['user']=='common', 'count'].sum()
    sum_of_individual = df['count'].sum()
    match_score = float(sum_of_common) / float(sum_of_individual)
    return '{0:.2f}%'.format(match_score*100)

# def get_word_count(username):
#     """Get a dataframe with word, count, and user, given a username."""
#     #get a list of tutples of srtings
#     title = db.session.query(Photo.title).filter(Photo.username==usernmae).all()
#     #get a list of strings
#     ls = [e for l in title for e in l]
#     #get a list of words
#     word_ls = [word for sentence in ls for word in sentence.split()]
#     #get word count 
#     counts = Counter(word_ls)
#     word_count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
#     word_count_df['user'] = pd.Series(username, index=word_count_df.index)
#     word_count_df.rename(columns={'index':'word', 0:'count', 'user':'user'}, inplace=True)
#     df = word_count_df.sort_values(by='count',ascending = False).head(20)
#     return df

if __name__ == "__main__":
    from flask import Flask, request, session
    from model import connect_to_db, db
    app = Flask(__name__)
    connect_to_db(app)