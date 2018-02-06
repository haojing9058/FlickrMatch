import requests
import json
from pprint import pprint
import os
from model import User, Photo
from model import connect_to_db, db

# global variable
API_KEY = os.environ['API_KEY']
API_URL = "https://api.flickr.com/services/rest"
RESPONSE_FORMAT = 'json&nojsoncallback=1'

# helper function for creating request
def get_req_base():
    return "%s?api_key=%s&format=%s"%(API_URL, API_KEY, RESPONSE_FORMAT)

def base_params():
    return {
            'api_key': API_KEY,
            'format': 'json',
            'nojsoncallback': '1',
        }


# def get_user_id_by_username (username):
#     """Get user_id from Flickr given a username"""

#     params = base_params()
#     params['method'] = "flickr.people.findByUsername"
#     params['username'] = username
#     response = requests.get(API_URL, params=params).json()
#     user_id = response['user']['nsid']
#     return user_id


# def get_userinfo_by_userid (user_id):
#     """Get user's info from Flickr given a user_id."""

def get_userinfo_by_username (username):
    """Get a user's info from Flickr given a username"""

    # Get Flickr user_id from Flickr given a username.
    params1 = base_params()
    params1['method'] = "flickr.people.findByUsername"
    params1['username'] = username
    response1 = requests.get(API_URL, params=params1).json()
    user_id = response1['user']['nsid']

    # Get the user's info given the Flickr user_id
    params2 = base_params()
    params2['method'] = "flickr.people.getInfo"
    params2['user_id'] = user_id
    response2 = requests.get(API_URL, params=params2).json()

    person = response2['person']
    photos = person['photos']

    realname = person['realname']['_content']
    user_location = person['location']['_content']
    photo_count = photos['count']['_content']
    photo_since = photos['firstdate']['_content']
    profile_url = person['profileurl']['_content']

    return User(user_id=user_id, username=username, realname=realname,
        user_location=user_location, photo_count=photo_count, photo_since=photo_since,
        profile_url=profile_url)


def get_popular_photos_by_userid(user_id, sort='interesting', per_page=9):
    """
    Get the most popular photos given a user_id.
    sort: One of faves, views, comments or interesting. Deafults to interesting.
    per_page: The maximum allowed value is 500.
    """

    params = base_params()
    params['method'] = "flickr.photos.getPopular"
    params['user_id'] = user_id
    params['sort'] = sort
    params['per_page'] = per_page
    response = requests.get(API_URL, params=params).json()

    # return a list of photos (photo_id) 
    photo_ids = []
    for i in response['photos']['photo']:
        photo_ids.append(i['id'])

    return photo_ids
    # Best nine to be displayed on webpage, more for text processing.


def get_photoinfo_by_photoid(photo_id):
    """return the photo info givin photo_id"""

    params = base_params()
    params['method'] = "flickr.photos.getInfo"
    params['photo_id'] = photo_id
    response = requests.get(API_URL, params=params).json()

    user_id = response['photo']['owner']['nsid']
    description = response['photo']['description']['_content']
    title = response['photo']['title']['_content']
    tags = []
    #use raw_tag or tag? 
    for i in response['photo']['tags']['tag']:
        # tags.append(i['raw'])
        tags.append(i['_content'])

    date_posted = response['photo']['dates']['posted']
    date_taken = response['photo']['dates']['taken']

    #geographic
    country = response['photo']['location']['country']['_content']
    place_id = response['photo']['location']['place_id']
    latitude = response['photo']['location']['latitude']
    longitude = response['photo']['location']['longitude']

    urls = []
    for url in response['photo']['urls']['url']:
        urls.append(url['_content'])











