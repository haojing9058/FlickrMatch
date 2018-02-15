

import pandas as pd
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db


def get_csv_tags(username1, username2):
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

        # word_count_df.columns = ['word','count','user']
        word_count_df.rename(columns={'index':'word', 0:'count', 'user':'user'}, inplace=True)
        df = word_count_df.sort_values(by='count',ascending = False).head(30)
        df = word_count_df.head(30)
        return df

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

    return result.to_csv(path_or_buf=r'static/tags.csv', header=False, index=False)

if __name__ == "__main__":
    from flask import Flask, request, session
    from model import connect_to_db, db
    app = Flask(__name__)
    connect_to_db(app)
