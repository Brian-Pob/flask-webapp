import random
import sys
import os
from flask import request, render_template, redirect, url_for, session, send_from_directory
from app import app, db
from app.models import User, Post, admins, liked_posts, disliked_posts
import json
import requests
from sqlalchemy import select, or_, insert, delete, update
import sqlalchemy
from flask_caching import Cache
import httpx
import asyncio
import ast
import spacy
nlp = spacy.load("en_core_web_lg")
cache = Cache(app)

base_url = 'https://hacker-news.firebaseio.com/v0/'

import datetime
@app.route("/")
def index():
    users = []
    uid = -1
    try:
        uinfo = dict(session).get('user', None)
        uinfo = dict(uinfo).get('userinfo', None)
        stmt = select(User.id).where(User.email == uinfo['email'])
        try:
            users = db.session.execute(stmt).first() 
            uid = users._asdict()['id']
            parsed = json.dumps((session), indent=4) 
        except Exception as e:
            print("Error in db access")
    except Exception as e:
        print(e)
        print("Error in user session")
    return render_template("land.html", session=dict(session).get('user', None), isadmin=isadmin(uid))
    
@app.route("/home")
def home():
    uid = get_user_id()
    posts = get_posts()
    myliked_posts = [i[1] for i in get_voted_posts(uid, vote_type="like")]
    mydisliked_posts = [i[1] for i in get_voted_posts(uid, vote_type="dislike")]
    current_time = datetime.datetime.now()
    for post in posts:
        time_posted = datetime.datetime.fromtimestamp(post['time'])
        time_since = current_time - time_posted
        hours, rem = divmod(time_since.seconds, 3600)
        post['time'] = hours
    sys.stdout.flush()
    return render_template(
        "home.html",
        session=dict(session).get('user', None),
        posts=posts, isadmin=isadmin(uid),
        liked_posts=myliked_posts, disliked_posts=mydisliked_posts
    )


def get_posts():
    with requests.Session() as s:
        top = s.get(base_url + "topstories.json").json()
        stories = [get_story_json(story_id, s) for story_id in top[0:100]]
        return stories

def get_story_json(story_id, s):
    @cache.memoize(timeout=604800) # one week
    def inner_get_json(story_id):
        extension = "item/" + str(story_id) + ".json"
        new_response = s.get(base_url + extension).json()
        doc = nlp(new_response['title'])
        new_response['keywords'] = []
        for i in doc.ents:
            if isinstance(i.text, list):
                new_response['keywords'] = i.text
            else:
                new_response['keywords'] = [i.text]
        if len(new_response['keywords']) < 2:
            rands = random.choices(new_response['title'].split(), k=2)
            new_response['keywords'] += rands
        sys.stdout.flush()
        return new_response
    return inner_get_json(story_id)

def get_voted_posts(uid, vote_type):
    stmt = ""
    res = ""
    if vote_type == "dislike":
        stmt = select(disliked_posts).where(disliked_posts.c.user_id==uid)
        res = db.session.execute(stmt).all()
    elif vote_type == "like":
        stmt = select(liked_posts).where(liked_posts.c.user_id==uid)
        res = db.session.execute(stmt).all()
    #res = [i[1] for i in res]
    sys.stdout.flush()

    return res

async def get_posts_async():
    async with httpx.AsyncClient() as s:
        top = (await s.get(base_url + 'topstories.json')).json()
        tasks = [
            s.get(base_url+'/item/'+str(article)+'.json')
            for article in top[0:10]
        ]
        posts = await asyncio.gather(*tasks)
        posts = [story.json() for story in posts]
        return posts

def isadmin(user_id):
    try:
        stmt = select(admins).where(admins.c.user_id == user_id)
        admin = db.session.execute(stmt).first()
        sys.stdout.flush()
        return admin != None
    except Exception as e:
        print(e)
        return False

@app.route("/about")
def about():
    return render_template(
            "about.html",
            session=dict(session).get('user', None),
            isadmin=isadmin(get_user_id())
        )

def get_user_id():
    users = []
    uid = -1
    try:
        uinfo = dict(session).get('user', None)
        uinfo = dict(uinfo).get('userinfo', None)
        stmt = select(User.id).where(User.email == uinfo['email'])
        try:
            users = db.session.execute(stmt).first()
            uid = users._asdict()['id']
            parsed = json.dumps((session), indent=4) 
            return uid
        except Exception as e:
            print("Error in db access")
    except Exception as e:
        print(e)
        print("Error in user session")

def vote(vote_type):

    uid = get_user_id()
    story_id = ""
    if request.method == 'POST':
        story_id = request.form[vote_type]
    
    story = {}
    with requests.Session() as s:
        story = get_story_json(story_id, s)
        newpost = Post(
            id=story['id'],
            post_type=story['type'],
            by=story['by'],
            title=story['title'],
            url=story.get('url', '')
        )
        try:
            db.session.add(newpost)
            print('test')
        except Exception as e:
            db.session.rollback()
        else:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                print("Integrity error")

    stmt = select(Post).where(Post.id==story['id'])
    mypost = db.session.execute(stmt).first()
    mypost = str(mypost[0])
    mypost = (ast.literal_eval(mypost))
    if vote_type == "dislike":
        stmt = (
            insert(disliked_posts).
            values(user_id=uid, post_id=mypost['id'])
        )
        rmstmt = (
            delete(liked_posts).
            where(
                liked_posts.c.user_id==uid,
                liked_posts.c.post_id==mypost['id']
            )
        )
    elif vote_type == "like":
        stmt = (
            insert(liked_posts).
            values(user_id=uid, post_id=mypost['id'])
        )
        rmstmt = (
            delete(disliked_posts).
            where(
                disliked_posts.c.user_id==uid,
                disliked_posts.c.post_id==mypost['id']
            )
        )

    try:
        db.session.execute(stmt)
        db.session.execute(rmstmt)
        db.session.commit()
    except Exception as e:
            db.session.rollback()
    else:
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("Integrity error")
            print("Except")


@app.route("/dislike", methods = ['POST'])
def dislike():
    vote("dislike")
    return redirect(request.referrer)

@app.route("/like", methods = ['POST'])
def like():
    vote("like")
    return redirect(request.referrer)

@app.route("/admin")
def admin():
    uid = get_user_id()
    if isadmin(uid):
        posts = get_posts_admin()
        all_posts = get_posts()
        for p in all_posts:
            if "url" not in p:
                p["url"] = ""

        users =  get_user_list()
        users_liked_posts = {}
        users_disliked_posts = {}
        for user_id in users:
            users_liked_posts[str(user_id)] = [i[1] for i in get_voted_posts(user_id, vote_type="like")]
            users_disliked_posts[str(user_id)] = [i[1] for i in get_voted_posts(user_id, vote_type="dislike")]

        filtered = filter(
            lambda post: post['id'] in [i[1] for i in posts],
            all_posts
        )
        posts_list = list(filtered)
        posts_data = {}
        for p in posts_list:
            posts_data[str(p["id"])] = p

        print(users_liked_posts)
        print(users_disliked_posts)
        return render_template(
            "admin.html",
            isadmin=isadmin(get_user_id()),
            session=dict(session).get('user', None),
            posts=posts,
            users=users,
            posts_data=posts_data,
            users_liked_posts=users_liked_posts,
            users_disliked_posts=users_disliked_posts
        )
    else:
        return redirect("/error")

@app.route("/profile")
def profile():
    uid = get_user_id()
    myliked_posts = [i[1] for i in get_voted_posts(uid, vote_type="like")]
    mydisliked_posts = [i[1] for i in get_voted_posts(uid, vote_type="dislike")]
    all_posts = get_posts()
    filtered = filter(
        lambda post: post['id'] in mydisliked_posts + myliked_posts,
        all_posts
    )
    myposts = list(filtered)
    current_time = datetime.datetime.now()
    for post in myposts:
        time_posted = datetime.datetime.fromtimestamp(post['time'])
        time_since = current_time - time_posted
        hours, rem = divmod(time_since.seconds, 3600)
        post['time'] = hours
    if uid:
        return render_template(
            "profile.html",
            session=dict(session).get('user', None),
            isadmin=isadmin(get_user_id()),
            posts=myposts,
            liked_posts=myliked_posts, disliked_posts=mydisliked_posts
        )
    else:
        return redirect("/error")

@app.route("/error")
def error():
    return render_template(
        "error.html",
        session=dict(session).get('user', None),
        isadmin=isadmin(get_user_id())
    )

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(
        os.path.join(app.root_path, 'static/images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/remove_dislike",methods= ['POST'] )
def remove_dislike():
    remove_vote('dislike')
    return redirect(request.referrer)

@app.route("/remove_like",methods= ['POST'] )
def remove_like():
    remove_vote('like')
    return redirect(request.referrer)

def remove_vote(vote_type):
    uid = get_user_id()
    story_id = ""

    if isadmin(uid):
        if request.method == 'POST':
            story_id, uid = request.form[vote_type].split("&")
    else:
        if request.method == 'POST':
            story_id = request.form[vote_type]
    
    stmt = select(Post).where(Post.id==story_id)
    mypost = db.session.execute(stmt).first()
    mypost = str(mypost[0])
    mypost = (ast.literal_eval(mypost))
    if vote_type == "dislike":
        rmstmt = (
            delete(disliked_posts).
            where(
                disliked_posts.c.user_id==uid,
                disliked_posts.c.post_id==mypost['id']
            )
        )
    elif vote_type == "like":
        rmstmt = (
            delete(liked_posts).
            where(
                liked_posts.c.user_id==uid,
                liked_posts.c.post_id==mypost['id']
            )
        )

    try:
        db.session.execute(rmstmt)
        db.session.commit()
    except Exception as e:
            db.session.rollback()
    else:
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("Integrity error")
            print("Except")

def get_posts_admin():
    lstmt = (
        select(liked_posts)
    )
    dstmt = (
        select(disliked_posts)
    )
    res = db.session.execute(lstmt).all()
    res += db.session.execute(dstmt).all()
    res.sort(key=lambda r:r[1])
    print(res)
    return res

def get_user_list():
    stmt = (
        select(User.id, User.email)
    )
    res = db.session.execute(stmt).all()
    res = listup_to_dict(res)
    print((res))
    return res

def listup_to_dict(listup):
    mydict = {}
    for user_id, username in listup:
        mydict[str(user_id)] = username

    return mydict
