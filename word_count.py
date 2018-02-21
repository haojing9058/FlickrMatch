import pandas as pd
import nltk
from nltk.corpus import stopwords
from string import punctuation
from sqlalchemy import create_engine
from string import punctuation
from collections import Counter
from model import User, Photo
from model import connect_to_db, db

STOP_WORDS = set(stopwords.words('english'))
SOCIAL_WORDS = set(['facebook', 'instagram', 'thanks', 'follow', 'share',
            'please', 'page', 'visit', 'thanks', 'feel'])

def users_word_count(username1, username2, text_type='tags'):
    """Return certain text_type of word counts for each user and their common word counts"""
    def count_word(username, text_type='tags'):
        """Return certain text_type of word counts dataframe for a given user.
        (string1, string2) --> dataframe
        text_type: options of "tags", title", "description". Defalt to "tags".
        """
        #get a list of tutples of srtings
        if text_type == 'tags':
            raw_data = db.session.query(Photo.tags).filter(Photo.username == username).all()
        elif text_type == 'title':
            raw_data = db.session.query(Photo.title).filter(Photo.username == username).all()
        elif text_type == 'description':
            raw_data = db.session.query(Photo.description).filter(Photo.username == username).all()
        # what if user do not use tags??
        #get a list of strings
        str_lst = [e for l in raw_data for e in l]
        #lower case and strip punctuations of a string
        str_lst_new = map(strip_punctuation, str_lst)
        #get a list of words
        word_ls = [w for sentence in str_lst_new for w in sentence.split()]
        #remove stop words
        filtered_words = [w for w in word_ls if not w in STOP_WORDS and SOCIAL_WORDS]
        #get word count dictionary
        counts = Counter(filtered_words)
        #convert dict to dataframe
        df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        #add "user" column to the dataframe
        df['user'] = pd.Series(username, index=df.index)
        #rename columns
        df.rename(columns={'index':'word', 0:'count', 'user':'user'}, inplace=True)
        #drop rows if word length is over 15
        df = df[df['word'].apply(lambda x: len(x) < 15)]
        #sort and select top 20
        df = df.sort_values(by='count',ascending = False).head(20)

        return df
    #word counts for each user
    words1 = count_word(username1, text_type)
    words2 = count_word(username2, text_type)

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
    df = pd.concat([words1, words2, common])

    return df

# def process_text(str):


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

def get_text_ls(file):
    """return a list of tags by common users"""
    pd.read_csv(file, )

def strip_punctuation (str):
    for p in list(punctuation):
        str = str.lower().replace(p, '')
    return str

if __name__ == "__main__":
    from flask import Flask, request, session
    from model import connect_to_db, db
    app = Flask(__name__)
    connect_to_db(app)
