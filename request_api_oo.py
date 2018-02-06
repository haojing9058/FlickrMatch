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


class User(object):
    """A user. """

    def __init__(self, username):
        self.username = username

        # get user_id from Flickr given a username
        params = base_params()
        params['method'] = "flickr.people.findByUsername"
        params['username'] = self.username
        # Question: is it okay to use try... except...?
        # try:
            # esponse = requests.get(API_URL, params=params).json()
        # except requests.exceptions.RequestException as e:
            # print e
        response = requests.get(API_URL, params=params).json()
        self.user_id = response['user']['nsid']

    def get_userinfo (self):
        """get user's info from Flickr given a user_id
        user's info: realname, user_location, photo_count, profile_url, first_date
        """
        params = base_params()
        params['method'] = "flickr.people.getInfo"
        params['user_id'] = self.user_id
        response = requests.get(API_URL, params=params).json()

        self.realname = response['person']['realname']['_content']
        self.user_location = response['person']['location']['_content']
        self.photo_count = response['person']['photos']['count']['_content']
        self.profile_url = response['person']['profileurl']['_content']
        self.photo_since = response['person']['photos']['firstdate']['_content']

    def get_popular_photos(self, sort='interesting', per_page=9):
        """get the most popular photos given a user_id.
        photo info: 
        sort: The sort order. One of faves, views, comments or interesting. Deafults to interesting.
        per_page: Number of photos to return per page. The maximum allowed value is 500
        """
        params = base_params()
        params['method'] = "flickr.photos.getPopular"
        params['user_id'] = self.user_id
        params['sort'] = sort
        params['per_page'] = per_page
        response = requests.get(API_URL, params=params).json()

        self.photo_ids = []
        for i in response['photos']['photo']:
            self.photo_ids.append(i['id'])

class Photo(object):
    """A photo. """
    def __init__ (self, photo_id):
        self.photo_id = photo_id

        params = base_params()
        params['method'] = "flickr.photos.getInfo"
        # Question: better way to handle photo_id?
        params['photo_id'] = self.photo_id
        response = requests.get(API_URL, params=params).json()

        self.description = response['photo']['description']['_content']
        self.title = response['photo']['title']['_content']
        self.tags = []
        #use raw_tag or tag? 
        for i in response['photo']['tags']['tag']:
            # tags.append(i['raw'])
            self.tags.append(i['_content'])

        self.date_posted = response['photo']['dates']['posted']
        self.date_taken = response['photo']['dates']['taken']

        #geographic
        self.country = response['photo']['location']['country']['_content']
        self.place_id = response['photo']['location']['place_id']
        self.lat = response['photo']['location']['latitude']
        self.lon = response['photo']['location']['longitude']

        self.urls = []
        for url in response['photo']['urls']['url']:
            self.urls.append(url['_content'])








