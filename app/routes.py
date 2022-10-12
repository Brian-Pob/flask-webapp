from flask import render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post
import requests

@app.route("/")
def index():
    #to_return = "<img src='/static/images/stars.jpg' alt='no image found'>"
    #image_url = url_for('memes', filename='spongebob-leak.gif')
    image_url = '/memes/spongebob-leak.gif'
    to_return = "<img src='%s' alt='no image found!!'>" % (image_url)
    session_user = dict(session).get('user', None)
    if (session_user):
        to_return = to_return + "<p>User {} is logged in</p>".format(session_user["userinfo"]["name"])
    return '<p>hello. This is a Python Flask app running with Gunicorn and Nginx! 🐍+🧪+🦄+🚙 = ⚡️💪🔥</p>' + to_return + image_url

@app.route("/home")
def home():
    # Testing
   # u = User(username='user2person', email='user2person@example.com')
    #assert not (u == None)
    #db.session.add(u)
    #db.session.commit()
    users = User.query.all()
    assert not (users == None)
    # End Testing
    return render_template("home.html", session=dict(session).get('user', None), users=users) 

@app.route("/apiTest")
def apiTest():
    base_url = 'https://hacker-news.firebaseio.com/v0/'
    response = requests.get(base_url + "topstories.json")
    to_return = []
    for i in range(10):
        extension = "item/" + str(response.json()[i]) + ".json?print=pretty"
        new_response = requests.get(base_url + extension)
        to_return.append(new_response.json()["title"])
    return '<h1>Hacker News API Data</h1>' + str(to_return)
