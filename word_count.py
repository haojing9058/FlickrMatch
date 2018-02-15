

import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db


def get_tags_df(username1, username2):
    def get_word_count(username):
        """Return tag words and count of given user.
        (string1, string2) --> dataframe
        """
        # what if user do not use tags??
        tags = db.session.query(Photo.tags).filter(Photo.username == username).all()
        #list of tuples
        tag_ls = [e for l in tags for e in l]#list of tags
        word_ls = [word for sentence in tag_ls for word in sentence.split()]#list of words
        counts = Counter(word_ls)
        word_count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        word_count_df['user'] = pd.Series(username, index=word_count_df.index)

        # word_count_df.columns = ['word','count','user']
        word_count_df.rename(columns={'index':'word', 0:'count', 'user':'user'}, inplace=True)
        df = word_count_df.sort_values(by='count',ascending = False).head(20)
        # df = word_count_df.head(30)
        return df

    words1 = get_word_count(username1)
    words2 = get_word_count(username2)
    common = words1.merge(words2, how='inner', on='word')
    common['count'] = common['count_x'] + common['count_y']
    common['user'] = 'common'
    common = common[['word', 'count', 'user']]

    words1 = words1.merge(words2, how='left', on='word')
    words1 = words1[words1['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    words1.columns = ['word','count','user']

    words2 = words2.merge(common, how='left', on='word')
    words2 = words2[words2['count_y'].isnull()].drop(['count_y', 'user_y'], axis=1)
    # words2 = words[['word', 'count_x', 'user_x'], columns=['word','count','user']]
    words2.columns = ['word','count','user']

    result = pd.concat([common, words1, words2])
    return result

def get_csv(df):
    """Save dataframe to .csv"""
    return result.to_csv(path_or_buf=r'static/tags.csv', header=False, index=False)

def calculate_match_score(df):
    """ Calculate match score given the "word, count, user" df.
    """
    sum_of_common = df.loc[df['user']=='common', 'count'].sum()
    sum_of_individual = df.loc['count'].sum()
    match_score = float(sum_of_common) / float(sum_of_individual)
    return '{0:.2f}%'.format(match_score*100)

if __name__ == "__main__":
    from flask import Flask, request, session
    from model import connect_to_db, db
    app = Flask(__name__)
    connect_to_db(app)
