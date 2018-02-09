import requests
import json
from pprint import pprint
import os
from model import User, Photo
from model import connect_to_db, db
import datetime

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


def get_user_by_username (username):
    """Get a user's info from Flickr given a username"""

    # Get Flickr user_id from Flickr given a username.
    params_find_by_username = base_params()
    params_find_by_username['method'] = "flickr.people.findByUsername"
    params_find_by_username['username'] = username
    response_username = requests.get(API_URL, params=params_find_by_username).json()
    user_id = response_username['user']['nsid']

    # Get the user's info given the Flickr user_id
    params_get_user_info = base_params()
    params_get_user_info['method'] = "flickr.people.getInfo"
    params_get_user_info['user_id'] = user_id
    response_userinfo = requests.get(API_URL, params=params_get_user_info).json()

    person = response_userinfo['person']
    photos = person['photos']

    # realname = person['realname']['_content']
    user_location = person['location']['_content']
    photo_count = photos['count']['_content']
    photo_since = datetime.datetime.fromtimestamp(int(photos['firstdate']['_content'])).strftime('%Y-%m-%d %H:%M:%S')

    profile_url = person['profileurl']['_content']

    return User(user_id=user_id, username=username, user_location=user_location, 
        photo_count=photo_count, photo_since=photo_since,
        profile_url=profile_url)


def get_photos_by_userid(user_id, sort='interesting', per_page=9):
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


def get_photo_by_photoid(photo_id):
    """return the photo info givin photo_id"""

    params = base_params()
    params['method'] = "flickr.photos.getInfo"
    params['photo_id'] = photo_id
    response = requests.get(API_URL, params=params).json()

    photo = response['photo']

    secret_id = photo['secret']
    server_id = photo['server']
    farm_id = photo['farm']
    img_url = 'https://farm' + str(farm_id) + '.staticflickr.com/' + server_id + '/' + photo_id + '_' + secret_id + '_s.jpg'

    user_id = photo['owner']['nsid']    
    title = photo['title']['_content']
    description = photo['description']['_content']
    tags = []
    #use raw_tag or tag? 
    for i in photo['tags']['tag']:
        # tags.append(i['raw'])
        tags.append(i['_content'])

    date = photo['dates']
    #fix the datetime format
    date_posted = datetime.datetime.fromtimestamp(int(date['posted'])).strftime('%Y-%m-%d %H:%M:%S')
    # date_posted = date['posted']
    date_taken = date['taken']

    #geographic
    if photo.get('location'):
        location = photo['location']
        country = location['country']['_content']
        place_id = location['place_id']
        lat = location['latitude']
        lon = location['longitude']
    else:
        country = None
        place_id = None
        lat = None
        lon = None

    url = photo['urls']['url'][0]['_content'].encode('utf-8')
    #type = photo['urls']['url'][0]['type']
    #'photopage'

    return Photo(photo_id=photo_id, user_id=user_id, title=title, 
        description=description, tags=tags, date_posted=date_posted,
        date_taken=date_taken, country=country, place_id=place_id,
        lat=lat, lon=lon, url=url, img_url=img_url)










