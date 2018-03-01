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
    # #get user id from Flickr api
    def helper(username):
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

    df_tags = word_count.users_word_count(username1, username2)
    word_count.get_tags_csv(df_tags)
    match_tags = word_count.get_match_score(df_tags)
    # text_url = "static/tags.csv"

    return render_template('bubble-page.html', 
                            username1 = username1,
                            username2 = username2,
                            match_tags=match_tags)

   
@app.route('/tags-bubble', methods=["POST"])
def display_partial_view():
    """Display bubble graph;
    display match score
    """
    # texttype = request.form.get('texttype') #get from dropdown menu
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    result = {}

    df_tags = word_count.users_word_count(username1, username2)
    # word_count.get_tags_csv(df_tags)
    result['match_tags'] = word_count.get_match_score(df_tags)

    df_title = word_count.users_word_count(username1, username2, text_type='title')
    word_count.get_title_csv(df_title)
    result['match_title'] = word_count.get_match_score(df_title)

    df_description = word_count.users_word_count(username1, username2, text_type='description')
    word_count.get_description_csv(df_description)
    result['match_description'] = word_count.get_match_score(df_description)

    #below is for recommendatio
    tags = word_count.get_tag_lst()
    text = word_count.get_text_lst()
    photo_ids = request_api.recommendation_by_text(tags, text)

    
    urls = []
    for photo_id in photo_ids:
        urls.append(db.session.query(Photo.url).filter(Photo.photo_id == photo_id).first())

    result['urls'] = urls

    return jsonify(result)


@app.route('/geo')
def display_map():
    
    username1 = request.args.get('username1')
    username2 = request.args.get('username2')
    word_count.get_geo_csv(word_count.geo(username1), word_count.geo(username2))

    return render_template('map.html',
                            username1=username1, 
                            username2=username2)

@app.route('/recommendation-geo')
def display_recommendation_geo():
    result = {}
    geo_lst = word_count.get_lat_lon()
    photo_ids = []
    for lat, lon in geo_lst:
       photo_ids += request_api.recommendation_by_geo(lat, lon, per_page=12) 
   
    urls = []
    for photo_id in photo_ids:
        urls.append(db.session.query(Photo.url).filter(Photo.photo_id == photo_id).first())

    result['urls'] = urls

    return jsonify(result)


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


# @app.route('/user-photos', methods=['POST'])
# def display_bestnine():
#     username1 = request.form.get('username1')
#     username2 = request.form.get('username2')
#     photos = {}
#     def helper(username):
#         """helper function to get the top 9 photo"""
#         #get user id from Flickr api
#         user = request_api.get_userid_by_username(username)
#         #get photo detail data from api and save to db
#         request_api.seed_photos_by_userid(user.user_id)
#         #select 9 photos from db
#         url_list = db.session.query(Photo.url).filter(Photo.username == username).limit(9).all()
#         # flat result to a list
#         return [e for l in url_list for e in l]

#     photos['url_list1'] = helper(username1)
#     photos['url_list2'] = helper(username2)

#     return jsonify(photos)

# @app.route('/tags-bubble')
# def display_rmd_photos():
#     """
#     Display recommended photos.
#     """
#     tags = word_count.get_tag_lst()
#     text = word_count.get_text_lst()
#     photo_ids = request_api.recommendation_by_text(tags, text)
#     urls = []
#     for photo_id in photo_ids:
#         # urls.append(db.session.query(Photo.url).get(photo_id).first())
#         db.session.query(Photo.url).filter(Photo.photo_id == '25174064667').first()
    
#     return render_template('rmd-img.html', urls=urls)

