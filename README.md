# FlickrMatch

FlickrMatch is a web application to explore common interests between two Flickr users. Using any two Flickr usernames, the app creates D3 word count graphs and match scores based on photo tags, title, and description, and a  D3 time-series map based on geo info of the photos.  The app also recommends pictures based on what they have in common. The app requests the users’ photo information from Flickr API and saves the data to the local database. The data is then structured and analyzed with pandas, nltk and reverse_geocoder libraries in Python. FlickrMatch is designed to create fun and socialization for Flickr users.

## Technology Stack
- Python (Flask, pandas, nltk, SQLAlchemy)
- Javascript (D3, AJAX, jQuery)
- PostgreSQL
- CSS
- HTML
- Bootstrap
## API
- Flickr API
## Features
### User Validation Check
Users must have valid Flickr usernames and have uploaded at least nine public accessible photos to use app features. When users enter the usernames, the app will call Flickr API’s to find user id by username. If the response return the status as “fail”, or the user forgets to enter Flickr username, the app will display alert using AJAX. 
### Best Nine
Once the user clicks “match”, the app will call Flickr API to get users’ photos information and store the data in the local database. It will display the most popular nine photos of each user, sorted by Flickr’s measure of “interesting”.
![Alt Text](static/bestnine.gif =417*258)
### Word Match and Recommendation
Users can see word match bubble graphs that show the frequency of users’ words used in their photo tags, title, and description, and the match score accordingly. The visualization is implemented by D3. In the back end, I use Python’s pandas and nltk to process the text data so that only the meaningful words are counted and sorted. Based on the most frequently used photo tags and words in common, the app calls Flickr API to get photo recommendation. 
### Path Match and Recommendation
Users can also see a path match - the users’ photo counts based on geological information and timeline. Given the latitude and longitude of a photo, the app uses Python reverse-geocoder to get the country code, and then combines Google Map countries_code.csv and structures the data using pandas. It gives each user’s photo counts in each country of each year. The recommendation is based on the countries that both users have been to, otherwise it will give the top visited countries of each user.
## Run FlickrMatch on your machine
Clone or fork this repo:
```sh
git clone https://github.com/haojing9058/FlickrMatch.git
cd flickrgram
```
Create and activate a virtual environment:
```sh
virtualenv env 
source env/bin/activate
```
Install:
```sh
pip install -r requirements.txt
```
Get an API key from Flickr (https://www.flickr.com/services/api/misc.api_keys.html).
Store the key in a file called secrets.sh.
Activate the secret key:
```sh
source secrets.sh
```
If you have PostgreSQL on your machine, create a database called flickrmatch and run the seed file:
```sh
createdb flickrmatch
python model.py
```
Run the server:
```sh
python server.py
```
Navigate to localhost:5000 in your browser.