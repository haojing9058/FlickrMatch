import requests
import json
from pprint import pprint
import os
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
# QUESTIONS: 
# 1. Make OO
# 2. try...except...

# class User(object):
#     """A user."""


def get_id_by_username (username):
    """get user_id from Flickr given a username"""

    params = base_params()
    params['method'] = "flickr.people.findByUsername"
    params['username'] = username
    response = requests.get(API_URL, params=params).json()
    user_id = response['user']['nsid']
    return user_id


def get_userinfo_by_userid (user_id):
    """get user's info from Flickr given a user_id
    user's info: realname, user_location, photo_count, profile_url, first_date
    """

    params = base_params()
    params['method'] = "flickr.people.getInfo"
    params['user_id'] = user_id
    response = requests.get(API_URL, params=params).json()
    realname = response['person']['realname']['_content']
    user_location = response['person']['location']['_content']
    photo_count = response['person']['photos']['count']['_content']
    profile_url = response['person']['profileurl']['_content']
    photo_since = response['person']['photos']['firstdate']['_content']


def get_popular_photos_by_userid(user_id, sort='interesting', per_page=9):
    """get the most popular photos given a user_id.
    photo info: 
    sort: The sort order. One of faves, views, comments or interesting. Deafults to interesting.
    per_page: Number of photos to return per page. The maximum allowed value is 500
    """

    params = base_params()
    params['method'] = "flickr.photos.getPopular"
    params['user_id'] = user_id
    params['sort'] = sort
    params['per_page'] = per_page
    response = requests.get(API_URL, params=params).json()

    # return a list of photos (photo_id) 
    photo_id_ls = []
    for i in response['photos']['photo']:
        photo_id_ls.append(i['id'])

    # Best nine to be displayed on webpage, more for text processing.


def get_photoinfo_by_photoid(photo_id):
    """return the photo info givin photo_id"""
    req = "%s?api_key=%s&format=%s&method=%s&photo_id=%s"%(API_URL, API_KEY, RESPONSE_FORMAT,
     "flickr.photos.getInfo", photo_id)

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









