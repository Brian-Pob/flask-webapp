from flask import render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post
import json
from sqlalchemy import select, or_

@app.route("/")
def index():
    #to_return = "<img src='/static/images/stars.jpg' alt='no image found'>"
    #image_url = url_for('memes', filename='spongebob-leak.gif')
    image_url = '/memes/spongebob-leak.gif'
    to_return = "<img src='%s' alt='no image found!!'>" % (image_url)
    to_return += "<a href='/login'>Login</a><a href='/home'>Home</a>"
    session_user = dict(session).get('user', None)
    if (session_user):
        to_return = to_return + "<p>User {} is logged in</p>".format(session_user["userinfo"]["name"])
    return '<p>This is a Python Flask app running with Gunicorn and Nginx! 🐍+🧪+🦄+🚙 = ⚡️💪🔥</p>' + to_return + image_url

@app.route("/home")
def home():
    # Testing
   # u = User(username='user2person', email='user2person@example.com')
    #assert not (u == None)
    #db.session.add(u)
    #db.session.commit()
    #users = db.one_or_404(db.select(User).filter_by(email='jayen@example.com')) 
    uinfo = dict(session).get('user', None)
    uinfo = dict(uinfo).get('userinfo', None)
    stmt = select(User)
    users = db.session.execute(stmt).first() 
    parsed = json.dumps((session), indent=4) 
    # End Testing
    return render_template("home.html", session=dict(session).get('user', None), users=users, parsed=parsed) 
