from flask import Flask, render_template, redirect, request, flash, session
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

    word_count.get_csv_tags('username1', 'username2')
    
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
   
@app.route('/tags-bubble')
def display_tags_bubble():
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    # word_count.get_csv_tags('username1', 'username2')
    
    return render_template('tags_draft.html')
# @app.route('/text-visual')
# def visualize_texts():
#     """visualize title, description and tags."""



#     # user1_id = request.args.get('user1_id')
#     # user2_id = request.args.get('user2_id')

#     # photo_ids_1 = request_api.get_photos_by_userid(user1_id, sort='views', per_page=30)
#     # for photo_id in photo_ids_1:
#     #     photo = request_api.get_photo_by_photoid(photo_id)
#     #     db_utils.add_photo(photo)

#     # photo_ids_2 = request_api.get_photos_by_userid(user2_id, sort='views', per_page=30)
#     # for photo_id in photo_ids_2:
#     #     photo = request_api.get_photo_by_photoid(photo_id)
#     #     db_utils.add_photo(photo)


#     return render_template('text-visual.html')

 # user_id1 = request_api.get_user_by_username(username2)

    # #add user into db
    # db_utils.create_user(user1)
    # db_utils.create_user(user2)

    # #obtain best_nine photos id for each user
    # photo_ids_1 = request_api.get_photos_by_userid(user1.user_id)
    # photo_ids_2 = request_api.get_photos_by_userid(user2.user_id)

    # # obtain best_nine photo_urls for each user
    # photos1_urls = []
    # for photo_id in photo_ids_1:
    #     photo = request_api.get_photo_by_photoid(photo_id)
    #     db_utils.add_photo(photo)
    #     img_url = photo.img_url
    #     photos1_urls.append(img_url)

    # photos2_urls = []
    # for photo_id in photo_ids_2:
    #     photo = request_api.get_photo_by_photoid(photo_id)
    #     db_utils.add_photo(photo)
    #     img_url = photo.img_url
    #     photos2_urls.append(img_url)


    


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

