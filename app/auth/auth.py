from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Blueprint, Flask, redirect, render_template, session, url_for
from app.auth import auth_bp as bp
from app import oauth, env, db
from app.models import User

@bp.route("/login")
def login():
    print(url_for("auth.callback", _external=True))
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True)
    )

@bp.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    uinfo = dict(session).get('user', None)
    uinfo = dict(uinfo).get('userinfo', None)
    if(db.session.execute(db.select(User).filter_by(email=uinfo.email,
        username=uinfo.email)).first() != None):
        print("Found old user")
        # To properly handle this, should clear session, logout, and redirect to
        # error page.
        return redirect("/")
    newuser = User(username=uinfo.email, email=uinfo.email)
    # Setting username = email for now.
    db.session.add(newuser)
    db.session.commit()    
    print("New user added to database")
    return redirect("/")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

