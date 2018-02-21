import requests
import json
from pprint import pprint
import os
import datetime
from model import User, Photo
from model import connect_to_db, db
import db_utils


# global variable
API_KEY = os.environ['API_KEY']
API_URL = "https://api.flickr.com/services/rest"
RESPONSE_FORMAT = 'json&nojsoncallback=1'

# helper function for creating request
def get_req_base():
    return "%s?api_ky=%s&format=%s"%(API_URL, API_KEY, RESPONSE_FORMAT)

def base_params():
    return {
            'api_key': API_KEY,
            'format': 'json',
            'nojsoncallback': '1',
        }

def get_userid_by_username(username):
    """Get a user's user id given a username"""
    if db.session.query(User).filter(User.username == username).first() is None:
        params_find_by_username = base_params()
        params_find_by_username['method'] = "flickr.people.findByUsername"
        params_find_by_username['username'] = username
        response_username = requests.get(API_URL, params=params_find_by_username).json()
        user_id = response_username['user']['nsid'].encode('utf-8')

        user = User(user_id=user_id, username=username)
        db_utils.create_user(user)

    else:
        user = db.session.query(User).filter(User.username == username).one()

    return user


def seed_photos_by_userid(user_id, sort='interesting', per_page=30):
    """
    Get photos given a user_id.
    sort: One of faves, views, comments or interesting.
    per_page: The maximum allowed value is 500.
    """
    params = base_params()
    params['method'] = "flickr.photos.getPopular"
    params['user_id'] = user_id
    params['sort'] = sort
    params['extras'] =','.join(['description','data_upload', 'date_taken', 'owner_name', 
    'last_update', 'geo', 'tags', 'views', 'media', 'url_sq'])
    params['per_page'] = per_page
    response = requests.get(API_URL, params=params).json()

    photos = response['photos']['photo']
    for p in photos:
        photo_id = p['id'].encode('utf-8')

        if db.session.query(Photo).get(photo_id) is None:
            user_id = p['owner'].encode('utf-8')
            username = p['ownername'].encode('utf-8')
            description = p['description']['_content'].encode('utf-8')
            tags = p['tags'].encode('utf-8')
            title = p['title'].encode('utf-8')
            views = p['views'].encode('utf-8')
            url = p['url_sq'].encode('utf-8')
            date_taken = p['datetaken'].encode('utf-8')
            date_upload = datetime.datetime.fromtimestamp(int(p['lastupdate'].encode('utf-8'))).strftime('%Y-%m-%d %H:%M:%S')
            media = p['media'].encode('utf-8')
            # lat = p['latitude']
            # lon = p['longitude']
            if p.get('place_id'):
                place_id = p['place_id'].encode('utf-8')
            else:
                place_id = None

            photo = Photo(photo_id=photo_id, user_id=user_id, username=username,
            description=description, tags=tags, title=title, views=views,
            url=url, date_taken=date_taken, date_upload=date_upload, place_id=place_id, media=media)
            
            db_utils.add_photo(photo)
        else:
            pass

# get recommendated photos based on text info
# tags, tag_mode, text, sort, content_type=1, machine_tags, media='photo', per_page=et
def recommendation_by_text(tags, text, per_page=24):
    """Get most relavent photos based on given text info(tags, title and description)
    tags: a comma-delimited list of tags
    text: list of words
    Add the photos into db if it's not in it, and return a list of photo_id.
    """
    params = base_params()
    params['method'] = "flickr.photos.search"
    params['tags'] = tags
    params['text'] = text
    params['sort'] = 'relevance'
    params['content_type'] = 1
    # params['machine_tags']
    # params['machine_tags_mode']
    params['media'] = 'photos'
    params['extras'] = 'url_sq'
    params['per_page'] = per_page
    response = requests.get(API_URL, params=params).json()

    photos = response['photos']['photo'] #a list of photos

    for p in photos:
        photo_ids = []
        photo_id = p['id'].encode('utf-8')
        photo_ids.append(photo_id)
        if db.session.query(Photo).get(photo_id) is None:
            # user_id = p['owner'].encode('utf-8')
            url = p['url_sq'].encode('utf-8')

            photo = Photo(photo_id=photo_id, url=url)

            db_utils.add_photo(photo)

        else:
            pass

    return photo_ids

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)


# def get_user_by_username (username):
#     """Get a user's info frm Flickr given a username"""

#     # Get Flickr user_id from Flickr given a username.
#     params_find_by_username = base_params()
#     params_find_by_username['method'] = "flickr.people.findByUsername"
#     params_find_by_username['username'] = username
#     response_username = requests.get(API_URL, params=params_find_by_username).json()
#     user_id = response_username['user']['nsid'].encode('utf-8')

#     # Get the user's info given the Flickr user_id
#     params_get_user_info = base_params()
#     params_get_user_info['method'] = "flickr.people.getInfo"
#     params_get_user_info['user_id'] = user_id
#     response_userinfo = requests.get(API_URL, params=params_get_user_info).json()

#     person = response_userinfo['person']
#     photos = person['photos']

#     # realname = person['realname']['_content']
#     if person.get('location'):
#         user_location = person['location']['_content'].encode('utf-8')
#     else:
#         user_location = None
#     photo_count = photos['count']['_content']
#     photo_since = datetime.datetime.fromtimestamp(int(photos['firstdate']['_content'])).strftime('%Y-%m-%d %H:%M:%S')

#     profile_url = person['profileurl']['_content'].encode('utf-8')

#     return User(user_id=user_id, username=username, user_location=user_location, 
#         photo_count=photo_count, photo_since=photo_since,
#         profile_url=profile_url)

# def get_photos_by_userid(user_id, sort='interesting', per_page=9):
#     """
#     Get the most popular photos given a user_id.
#     sort: One of faves, views, comments or interesting. Deafults to interesting.
#     per_page: The maximum allowed value is 500.
#     """

#     params = base_params()
#     params['method'] = "flickr.photos.getPopular"
#     params['user_id'] = user_id
#     params['sort'] = sort
#     params['per_page'] = per_page
#     response = requests.get(API_URL, params=params).json()

#     # return a list of photos (photo_id) 
#     photo_ids = []
#     for i in response['photos']['photo']:
#         photo_ids.append(i['id'].encode('utf-8'))

#     return photo_ids
#     # Best nine to be displayed on webpage, more for text processing.


# def get_photo_by_photoid(photo_id):
#     """return the photo info givin photo_id"""

#     params = base_params()
#     params['method'] = "flickr.photos.getInfo"
#     params['photo_id'] = photo_id
#     response = requests.get(API_URL, params=params).json()

#     photo = response['photo']

#     secret_id = photo['secret'].encode('utf-8')
#     server_id = photo['server'].encode('utf-8')
#     farm_id = photo['farm']
#     img_url = 'https://farm' + str(farm_id) + '.staticflickr.com/' + server_id + '/' + photo_id + '_' + secret_id + '_s.jpg'

#     user_id = photo['owner']['nsid'].encode('utf-8')
#     title = photo['title']['_content'].encode('utf-8')
#     description = photo['description']['_content'].encode('utf-8')
#     tags = []
#     #use raw_tag or tag? 
#     for i in photo['tags']['tag']:
#         # tags.append(i['raw'])
#         tags.append(i['_content'].encode('utf-8'))

#     date = photo['dates']
#     #fix the datetime format
#     date_posted = datetime.datetime.fromtimestamp(int(date['posted'])).strftime('%Y-%m-%d %H:%M:%S')
#     # date_posted = date['posted']
#     date_taken = date['taken'].encode('utf-8')

#     #geographic
#     if photo.get('location'):
#         location = photo['location']
#         country = location['country']['_content'].encode('utf-8')
#         place_id = location['place_id'].encode('utf-8')
#         lat = location['latitude'].encode('utf-8')
#         lon = location['longitude'].encode('utf-8')
#     else:
#         country = None
#         place_id = None
#         lat = None
#         lon = None

#     url = photo['urls']['url'][0]['_content'].encode('utf-8')
#     #type = photo['urls']['url'][0]['type']
#     #'photopage'

#     return Photo(photo_id=photo_id, user_id=user_id, title=title, 
#         description=description, tags=tags, date_posted=date_posted,
#         date_taken=date_taken, country=country, place_id=place_id,
#         lat=lat, lon=lon, url=url, img_url=img_url)










