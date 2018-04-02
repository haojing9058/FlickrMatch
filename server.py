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

@app.route('/', methods=['GET'])
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/user-check', methods=['POST'])
def check_username():
    # """check if username valid from Flickr."""
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')

    check = {}

    #get user id from Flickr api
    def helper(username):
        if username == "":
            return 'empty'

        user = request_api.get_userid_by_username(username)
        if user == 'fail':
            return 'fail'

    check['username1_ck'] = helper(username1)
    check['username2_ck'] = helper(username2)

    return jsonify(check)


@app.route('/userinfo', methods=['POST'])
def display_userinfo():
    """User info page."""
   
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    name1 = request.form.get('name1')
    name2 = request.form.get('name2')
    
    def helper(username):
        """helper function to get the top 9 photo"""
        #get user id from Flickr api
        user = request_api.get_userid_by_username(username)
        #get photo detail data from api and save to db
        request_api.seed_photos_by_userid(user.user_id)
        #select 9 photos from db, get a list of tuples
        url_list_tp = db.session.query(Photo.url).filter(Photo.username == username).limit(9).all()
        # flat result to a list
        url_list = [e for l in url_list_tp for e in l]

        return url_list

    # import pdb; pdb.set_trace()
    url_list1 = helper(username1)
    url_list2 = helper(username2)

    print "urls1:"
    print url_list1
    print "urls2:"
    print url_list2

    return render_template('userinfo.html', 
                            username1 = username1,
                            username2 = username2,
                            name1=name1,
                            name2=name2,
                            urls1 = url_list1,
                            urls2 = url_list2)


@app.route('/tags-bubble', methods=["GET"])
def display_tags_bubble():
    """Display a bubble graph and match score based on tags
    """
    username1 = request.args.get('username1')
    username2 = request.args.get('username2')
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')

    df_tags = word_count.users_word_count(username1, username2)
    word_count.get_tags_csv(df_tags)
    match_tags = word_count.get_match_score(df_tags)

    return render_template('bubble-page.html', 
                            username1 = username1,
                            username2 = username2,
                            name1=name1,
                            name2=name2,
                            match_tags=match_tags)

   
@app.route('/tags-bubble', methods=["POST"])
def display_partial_view():
    """Display bubble graphs and match scores based on tags, title, and description.
    """

    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    result = {}

    df_tags = word_count.users_word_count(username1, username2)
    result['match_tags'] = word_count.get_match_score(df_tags)

    df_title = word_count.users_word_count(username1, username2, text_type='title')
    word_count.get_title_csv(df_title)
    result['match_title'] = word_count.get_match_score(df_title)

    df_description = word_count.users_word_count(username1, username2, text_type='description')
    word_count.get_description_csv(df_description)
    result['match_description'] = word_count.get_match_score(df_description)

    #get recommendated photo_ids
    tags = word_count.get_tag_lst()
    text = word_count.get_text_lst()
    result['tags'] = tags
    result['text'] = text
    photo_ids = request_api.recommendation_by_text(tags, text)
    result['photo_ids'] = photo_ids
    
    urls = []
    for photo_id in photo_ids:
        urls.append(db.session.query(Photo.url).filter(Photo.photo_id == photo_id).first())
    result['urls'] = urls

    return jsonify(result)


@app.route('/geo')
def display_map():
    """Disply location match in timeline.
    """
    username1 = request.args.get('username1')
    username2 = request.args.get('username2')
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    word_count.get_geo_csv(word_count.geo(username1), word_count.geo(username2))

    return render_template('map.html',
                            username1=username1, 
                            username2=username2,
                            name1=name1,
                            name2=name2)

@app.route('/recommendation-geo')
def display_recommendation_geo():
    """Get recommendated photo_ids based on location common countries the users visited.
    """
    result = {}
    geo_lst = word_count.get_lat_lon()

    urls = []
    for lat, lon in geo_lst:
        if len(geo_lst) == 2:
            photo_ids = request_api.recommendation_by_geo(lat, lon, per_page=18)
        else:
            photo_ids = request_api.recommendation_by_geo(lat, lon, per_page = 36)
        for photo_id in photo_ids:
            urls.append(db.session.query(Photo.url).filter(Photo.photo_id == photo_id).first())

    result['urls'] = urls
    result['geo_lst'] = geo_lst

    return jsonify(result)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')