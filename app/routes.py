from flask import render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post
import json
import requests
from sqlalchemy import select, or_
import datetime

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
    return '<p>hello. This is a Python Flask app running with Gunicorn and Nginx! 🐍+🧪+🦄+🚙 = ⚡️💪🔥</p>' + to_return + image_url

@app.route("/home")
def home():
    users = []
    try:
        uinfo = dict(session).get('user', None)
        uinfo = dict(uinfo).get('userinfo', None)
        stmt = select(User)
        try:
            users = db.session.execute(stmt).first() 
            parsed = json.dumps((session), indent=4) 
        except:
            print("Error in db access")
    except:
        print("Error in user session")

    base_url = 'https://hacker-news.firebaseio.com/v0/'
    response = requests.get(base_url + "topstories.json")
    to_return = []
    for i in range(10):
        extension = "item/" + str(response.json()[i]) + ".json?print=pretty"
        new_response = requests.get(base_url + extension)
        temp_response = new_response.json()
        current_time = datetime.datetime.now()
        time_posted = datetime.datetime.fromtimestamp(temp_response['time'])
        time_since = current_time - time_posted
        hours, rem = divmod(time_since.seconds, 3600)
        temp_response['time'] = hours
        to_return.append(temp_response)

    return render_template("home.html", session=dict(session).get('user', None), users=users, posts=to_return) 
