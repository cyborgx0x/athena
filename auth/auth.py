from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db
from .form import RegistrationForm, LoginForm
from werkzeug.urls import url_parse
import urllib.parse
import requests
import json
import datetime

auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder='static')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a registered user!')
        return redirect(url_for('auth_bp.login'))
    return render_template('reg.html', title='Register', form=form)



@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form = form)

@auth_bp.route("/login_with_facebook", methods=['GET','POST'])
def login_with_facebook():
    client_id = "716233336363436"
    state = request.referrer
    redirect_url = "https://athena-publication.herokuapp.com/auth"
    link = "https://www.facebook.com/v14.0/dialog/oauth?" + "client_id=" + client_id + "&redirect_uri=" + redirect_url + "&state=" + state
    return redirect(link)

@auth_bp.route('/auth')
def auth():
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
            user = User.query.filter_by(facebook=id).first()
            if user is None:
                new_user = User(facebook=id, name=name, email=email)
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


    
@auth_bp.route("/api/v1/auth", methods=["POST"])
def authentication():
    
    data = json.loads(request.data.decode("UTF-8"))
    username = data["username"]
    password = data["password"]
    if username != "admin":
        return Response(response="Not Found", status=401)
    response = {
    'id': 1,
    'name': "Thuan Nguyen",
    'username': 'admin',
    'password': '',
    'avatar': 'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png',
    'status': 1,
    'telephone': '',
    'lastLoginIp': '27.154.74.117',
    'lastLoginTime': 1534837621348,
    'creatorId': 'admin',
    'createTime': 1497160610259,
    'deleted': 0,
    'roleId': 'admin',
    'lang': 'zh-CN',
    'token': '4291d7da9005377ec9aec4a71ea837f'
    }
    return {"result": response}

@auth_bp.route("/api/v1/user/info", methods=["GET"])
def get_user_info():
    user_info = {
        "id": '4291d7da9005377ec9aec4a71ea837f',
        "name": '天野远子',
        "username": 'admin',
        "password": '',
        "avatar": '/avatar2.jpg',
        "status": 1,
        "telephone": '',
        "lastLoginIp": '27.154.74.117',
        "lastLoginTime": 1534837621348,
        "creatorId": 'admin',
        "createTime": 1497160610259,
        "merchantCode": 'TLif2btpzg079h15bk',
        "deleted": 0,
        "roleId": 'admin',
        "role": {}
    }
    return {"result": user_info}