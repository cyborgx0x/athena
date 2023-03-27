from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, Response, jsonify)
from flask_login import current_user, login_user, logout_user
from app import db
from werkzeug.urls import url_parse
import urllib.parse
import requests
import json
import datetime
from auth.models import CoreUser
import os
from app.request import Request
from flask_praetorian import Praetorian
from auth.models import CoreUser
from app import app
guard = Praetorian()
guard.init_app(app, CoreUser)

   
auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder='static')

from app.views import register_api
register_api(app=auth_bp, model=CoreUser, name="users")


'''
Authentication
'''

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

class RegisterRequest(Request):
    class Meta:
        register_fields=dict(
            username="username",
            name="name",
            email="email",
            avatar="avatar",
            about_me="about_me",
            password="password",
        )

@auth_bp.post('/register')
def register():
    if current_user.is_authenticated:
        return jsonify(dict(
            detail="Already Login"
        ), status=400)
    handler = RegisterRequest()
    data = handler.to_json(load_of_data=request.json)
    users = CoreUser.query.filter_by(username=data["username"]).first()
    if users:
        return jsonify(dict(
            detail="Username already taken"
        )) 
    password = data.pop("password")
    user = CoreUser(**data)
    user.password_hash = guard.hash_password(password)
    del password
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())


class LoginRequest(Request):
    class Meta:
        register_fields = dict(
            username="user_name",
            password="password"
        )

     

@auth_bp.post('/login')
def login():
    req = request.get_json(force=True)
    username = req.get("username", None)
    password = req.get("password", None)
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)


@auth_bp.get("/login_with_facebook")
def login_with_facebook():
    client_id = os.getenv("FACEBOOK_CLIENT_ID")
    state = request.referrer
    redirect_url = os.getenv("REDIRECT_URL")
    link = "https://www.facebook.com/v14.0/dialog/oauth?" + "client_id=" + client_id + "&redirect_uri=" + redirect_url + "&state=" + state
    return redirect(link)

@auth_bp.route('/auth')
def auth():
    client_secret = os.getenv("CLIENT_SECRET")
    code = request.args.get("code")
    redirect_link = request.args.get("state", url_for("index"))
    redirect_link = urllib.parse.unquote(redirect_link)
    print("redirect:" + redirect_link)
    link_referal = request.referrer
    print("link referal:" + str(link_referal))
    ex_token = "https://graph.facebook.com/v14.0/oauth/access_token?client_id=716233336363436&redirect_uri=https://athena-publication.herokuapp.com/auth&client_secret=530a79a255d5f568bc62ad10be922f17&code="+code
    acc = requests.get(ex_token)
    print(acc.text)
    if acc.status_code == 200:
        r = json.loads(acc.text)
        access_token = r["access_token"]
        graph_link = "https://graph.facebook.com/v14.0/me?fields=id%2Cname%2Cemail%2Cpicture&access_token=" + access_token
        long_token = "https://graph.facebook.com/v14.0/oauth/access_token?grant_type=fb_exchange_token&client_id=716233336363436&client_secret=530a79a255d5f568bc62ad10be922f17&fb_exchange_token=" + access_token
        avatar_url = "https://graph.facebook.com/v14.0/me/picture?fields=url&redirect=false&transport=cors&width=480&access_token=" + access_token
        ava = requests.get(avatar_url)
        auth = requests.get(graph_link)
        long_token_gen = requests.get(long_token)
        print(auth)
        print(long_token_gen)
        if auth.status_code == 200:
            r = json.loads(auth.text)
            print(r)
            id = r['id']
            name = r['name']
            email = r['email']
            avatar = json.loads(ava.text)["data"]["url"]
            user = CoreUser.query.filter_by(facebook=id).first()
            if user is None:
                new_user = CoreUser(facebook=id, name=name, email=email)
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)
                login_user(new_user)
                return redirect(link_referal)
            user.email = email
            user.avatar = str(avatar)
            user.last_seen = datetime.now()
            db.session.commit()
            login_user(user)
            return redirect(link_referal)
    return redirect(url_for("index"))
