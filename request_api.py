import requests
import json
from pprint import pprint
import os
# global variable
API_KEY = os.environ['API_KEY']
# API_KEY = "bb72104f20be45b61f672cfa885c1b4a"
#put this into secret file later

API_URL = "https://api.flickr.com/services/rest"
RESPONSE_FORMAT = 'json&nojsoncallback=1'

# helper function for creating request

def get_id_by_username (username):
    """get user_id from Flickr given a username"""
    req = "%s?api_key=%s&format=%s&method=%s&username=%s"%(API_URL, API_KEY, RESPONSE_FORMAT,
     "flickr.people.findByUsername", username)
    response = requests.get(req).json()
    user_id = response['user']['nsid']
    return user_id


def get_userinfo_by_userid (user_id):
    """get user's info from Flickr given a user_id
    user's info: realname, user_location, photo_count, profile_url, first_date
    """
    req = "%s?api_key=%s&format=%s&method=%s&user_id=%s"%(API_URL, API_KEY, RESPONSE_FORMAT,
     "flickr.people.getInfo", user_id)
    response = requests.get(req).json()
    realname = response['person']['realname']['_content']
    user_location = response['person']['location']['_content']
    photo_count = response['person']['photos']['count']['_content']
    profile_url = response['person']['profileurl']['_content']
    first_date = response['person']['photos']['firstdate']['_content']


def get_popular_photos_by_userid(user_id, sort='interesting', per_page=9):
    """get the most popular photos given a user_id.
    photo info: 
    sort: The sort order. One of faves, views, comments or interesting. Deafults to interesting.
    per_page: Number of photos to return per page. The maximum allowed value is 500
    """
    req = "%s?api_key=%s&format=%s&method=%s&user_id=%s&sort=%s&per_page=%s"%(API_URL, 
        API_KEY, RESPONSE_FORMAT,"flickr.photos.getPopular", user_id, sort, per_page)

    response = requests.get(req).json()

    # return a list of photos (photo_id, user_id) 
    # - Best nine to be displayed on webpage.


def get_photoinfo_by_photoid(photo_id):
    """return the photo info givin photo_id"""
    req = "%s?api_key=%s&format=%s&method=%s&photo_id=%s"%(API_URL, API_KEY, RESPONSE_FORMAT,
     "flickr.photos.getInfo", photo_id)

    response = requests.get(req).json()

    return response

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









