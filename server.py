from flask import Flask, render_template, redirect, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Photo
import request_api
import db_utils
import word_count

app = Flask(__name__)
app.secret_key = '\xf5\xf8\xb0t\x02\xdf\xd5\x7f\xbe1$P\xb4\xed\xfc k\xd4:\xa4\x96\x852h' 
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/userinfo', methods=['POST'])
def display_userinfo():
    """User info page."""
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    
    def helper(username):
        """helper function to get the top 9 photo"""
            #get user id from Flickr api
        user = request_api.get_userid_by_username(username)
        #get photo detail data from api and save to db
        request_api.seed_photos_by_userid(user.user_id)
        #select 9 photos from db
        url_list = db.session.query(Photo.url).filter(Photo.username == username).limit(9).all()
        # flat result to a list
        return [e for l in url_list for e in l]

    url_list1 = helper(username1)
    url_list2 = helper(username2)

    return render_template('userinfo.html', 
                            username1 = username1,
                            username2 = username2,
                            urls1 = url_list1,
                            urls2 = url_list2)


@app.route('/tags-bubble', methods=["GET"])
def display_tags_bubble():
    """Display bubble graph;
    display match score
    """
    username1 = request.args.get('username1')
    username2 = request.args.get('username2')

    df = word_count.users_word_count(username1, username2)
    word_count.get_tags_csv(df)
    match_score = word_count.get_match_score(df)
    # text_url = "static/tags.csv"

    return render_template('tags_draft.html', 
                            username1 = username1,
                            username2 = username2,
                            match_score=match_score)

   
@app.route('/tags-bubble', methods=["POST"])
def display_partial_view():
    """Display bubble graph;
    display match score
    """
    texttype = request.form.get('texttype') #get from dropdown menu
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    text_url = {}

    if texttype == "tags":
        # df = word_count.get_tags_df(username1, username2)
        # word_count.get_tags_csv(df)
        # match_score = word_count.get_match_score(df)
        text_url = "static/tags.csv"

    elif texttype == "title":
        df = word_count.users_word_count(username1, username2, text_type='title')
        word_count.get_title_csv(df)
        # match_score = word_count.get_match_score(df)
        text_url = "static/title.csv"

    elif texttype == "description":
        df = word_count.users_word_count(username1, username2, text_type='description')
        word_count.get_description_csv(df)
        # match_score = word_count.get_match_score(df)
        text_url = "static/description.csv"

    return text_url
    # return render_template('tags_draft.html', 
    #                 username1 = username1,
    #                 username2 = username2,
    #                 match_score=match_score,
    #                 text_url = text_url)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

