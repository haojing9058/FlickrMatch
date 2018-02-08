from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Photo
import request_api
import db_utils

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
    name1 = request.form.get('username1')
    name2 = request.form.get('username2')

    user1 = request_api.get_user_by_username(name1)
    user2 = request_api.get_user_by_username(name2)
    
    db_utils.create_user(user1)
    db_utils.create_user(user2)

    return render_template('userinfo.html', 
                            user1 = user1,
                            user2 = user2)


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

