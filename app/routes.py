import json, os
import re
import io
from flask import (Flask, Markup, flash, jsonify, redirect, render_template,
                   request, send_file, url_for, session)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from tools import *
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_parse
import ast
import requests
from app import app, db
from app.form import (LoginForm,
                      RegistrationForm)
from app.models import (Collection, Media, User)
from datetime import datetime
import urllib.parse

@app.route("/")
def index():
    top_view_collections = Collection.query.filter_by(status="public").order_by(Collection.id.desc()).limit(20).all()
    top_creators = User.query.limit(12).all()
    return  render_template("home.html", top_view_collections = top_view_collections, top_creators=top_creators)

@app.route("/editor")
def editor():
    return render_template('editor.html')

@app.route('/privacy-policy')
def pp():
    return render_template('pp.html')

@app.route('/TOS')
def tos():
    return render_template('TOS.html')

@app.route("/test/search/", methods=['GET', 'POST'])
def test_search():
    return render_template('_search.html')

'''
function area
chứa những chức năng mở rộng
'''

@app.route("/img-cover/<path:link>")
def img_proxy(link):
    img = return_img(link)
    img.seek(0)
    return  send_file(img, mimetype='image/jpeg')

@app.route("/upload_link",methods = ['GET', 'POST'])
def upload_image_by_link():
    if request.method == "POST":
        link = json.loads(request.data.decode("UTF-8"))["url"]
        file  = getimage(link)
        print(file)
        res = upload(file)
        print(type(res), res)
        r = {
            "success" : 1,
            "file": {
                "url" : res["data"]["image"]["url"],
            }
        }
        return r

@app.route("/upload_image",methods = ['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        file  = request.files["image"]
        data  = file
        res = upload(data)
        print(res)
        r = {
            "success" : 1,
            "file": {
                "url" : res["data"]["image"]["url"],
            }
        }
        return r

@login_required
@app.route("/edit/user/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        if incoming_data["type"] == "content":
            return jsonify(user.about_me)
        elif incoming_data["type"] == "upload":
            user.about_me =incoming_data["value"]
            db.session.commit()
            return "success 🔥🔥🔥"
        elif incoming_data["type"] == "user_full_name":
            user.name = incoming_data["value"]
            db.session.commit()
            return "Cập nhật thành công tên 🔥🔥🔥"
        elif incoming_data["type"] == "user_avatar":
            user.avatar = incoming_data["value"]
            db.session.commit()
            return "Cập nhật thành công avatar 🔥🔥🔥"
    if current_user.id == user.id:
        return render_template("edit_user.html", user = user)
    else:
        return redirect(url_for("index"))


@app.route("/all_collections")
def all_collections():
    all_collections = Collection.query.filter_by(status="public")
    return  render_template("all_collections.html", all_collections = all_collections, title =  "Tất cả tác phẩm")

@app.route("/collection/<int:id>/", methods=['GET', 'POST'])
def public_collection(id):
    collection = Collection.query.filter_by(id=id).first()
    medias = Media.query.filter_by(collection_id=id).order_by(Media.id)
    tags = collection.tag_render()
    for tag in tags:
        pass
    return  render_template("public_collection.html", collection = collection, medias = medias)

@app.route("/user/<user_id>")
def user_profile(user_id):
    collections = Collection.query.filter_by(creator_id = user_id, status = "public")
    user = User.query.filter_by(id = user_id).first()
    return render_template("user.html", collections = collections, user = user)

@app.route("/year/<publish_year>")
def year_view(publish_year):
    collections = Collection.query.filter_by(publish_year = publish_year)
    return render_template("all_collections.html", all_collections = collections, title = publish_year +  ": Tất cả tác phẩm")

@app.route("/tag/<tag>")
def tag_view(tag):
    collections = Collection.query.filter(Collection.tag.like("%" + tag + "%"))
    return render_template("all_collections.html", all_collections = collections, title = tag +  ": Tất cả tác phẩm")

@app.route("/edit/collection/<int:id>/", methods=['GET', 'POST'])
@login_required
def edit_collection(id):
    collection = Collection.query.filter_by(id=id).first()
    if request.method == 'POST':
       
        incoming_data= json.loads(request.data.decode('UTF-8'))
        if incoming_data["type"] == "content":
            return jsonify(collection.desc)
        elif incoming_data["type"] == "upload":
            try: 
                collection.desc = incoming_data["value"]
                print(collection.desc)
                db.session.commit()
                return "Đã cập nhật nội dung"
            except:
                return "incoming data invalid"
        elif incoming_data["type"] == "publish_year":
            collection.publish_year = incoming_data["value"]
            db.session.commit()
            return "year updated"
        elif incoming_data["type"] == "collection_name":
            collection.name = incoming_data["value"]
            db.session.commit()
            return "name updated"
        elif incoming_data["type"] == "tag-manage":
            collection.tag = incoming_data["value"]
            db.session.commit()
            return "tag updated"
        elif incoming_data["type"] == "author":
            input_author = incoming_data["value"]
            collection.author = input_author
            db.session.commit()
            return "added author"
        elif incoming_data["type"] == "book-cover":
            collection.cover = incoming_data["value"]
            collection.render_cover()
            db.session.commit()
            return "Đã cập nhật ảnh bìa"
        elif incoming_data["type"] == "short-desc":
            collection.short_desc = incoming_data["value"]
            db.session.commit()
            return "Mô tả ngắn được cập nhật"
        elif incoming_data["type"] == "collection-author":
            collection.author_id = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật tác giả"
        elif incoming_data["type"] == "download":
            collection.download = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật link download"
        elif incoming_data["type"] == "collection-status":
            collection.status = incoming_data["value"]
            db.session.commit()
            if collection.status == "public":
                return "Đã thay đổi trạng thái thành: Công khai"
            else:
                return "Đã trở về bản nháp"
    print(current_user.id, collection.creator_id)
    if current_user.id == collection.creator_id or current_user.type == 1:
        return  render_template("edit_collection.html", collection = collection)
    else:
        return  redirect(url_for("index"))


@app.route("/collection/<collection_name>/")
def specific_collection_name(collection_name):
    collection = Collection.query.filter_by(name=collection_name).first()
    return  render_template("viewer.html", collection = collection)


@app.route("/media/<int:id>/")
def public_media(id):
    chapter = Media.query.filter_by(id=id).first()
    if chapter.view:
        chapter.view += 1
    else:
        chapter.view = 1
    db.session.commit()
    collection = chapter.collection
    chapters = Media.query.filter_by(type="chapter", collection_id=collection.id).order_by(Media.name)
    return render_template('public_media.html', chapter = chapter, collection=collection, chapters = chapters)



@app.route("/edit/media/<int:id>/", methods=['GET', 'POST'])
@login_required
def edit_media(id):
    chapter = Media.query.filter_by(id=id).first()
    if request.method == 'POST':
        incoming_data = json.loads(request.data.decode('UTF-8'))
        if incoming_data["type"] == "chapter_name":
            chapter.name = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật tên chương"
        if incoming_data["type"] == "chapter_order":
            chapter.chapter_order = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật thứ tự"
        elif incoming_data["type"] == "content":
            return jsonify(chapter.content)
        elif incoming_data["type"] == "upload":
            chapter.content = incoming_data["value"]
            print(chapter.content)
            db.session.commit()
            return "Đã cập nhật nội dung chương"
    if current_user.id == chapter.user_id or current_user.type == 1:
        return render_template('edit_media.html', chapter=chapter)
    else:
        return redirect(url_for("dashboard"))




'''
API SESSION
Contain interaction with the request from client
'''


@app.route("/editor/<int:collection_id>/new-chapter/", methods=['GET', 'POST'])
def new_chapter(collection_id):
    # if current_user.type == 1:
    new_chapter = Media(name="New Media", collection_id=collection_id, user_id=current_user.id, type="chapter")
    db.session.add(new_chapter)
    db.session.commit()
    db.session.refresh(new_chapter)
    return redirect(url_for('edit_media', id=new_chapter.id))


@app.route("/build_indexing/", methods=['GET', 'POST'])
def build_indexing():
    collections=Collection.query.all()
    authors = User.query.all()
    if request.method=='POST':
        incoming_data = json.loads(request.data.decode('UTF-8'))
        if incoming_data["query"] == "author":
            return jsonify(authors)           
    return jsonify(collections)


@app.route("/new_collection/", methods=['GET', 'POST'])
def new_collection():
    new_collection = Collection(name="Tác phẩm mới", creator_id=current_user.id)
    db.session.add(new_collection)
    db.session.commit()
    db.session.refresh(new_collection)
    return redirect(url_for('edit_collection', id=new_collection.id))


@app.route("/delete", methods=['GET', 'POST'])
def delete_item():
    return


'''
User Session
Contain route about user authentication, profile, configuration and dashboard
'''
@app.route('/authorized', methods=['GET','POST'])
def authorized():
    access_token = request.args.get("access_token")
    print("facebook")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
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

@app.route("/login_with_facebook", methods=['GET','POST'])
def login_with_facebook():
    client_id = "716233336363436"
    state = request.referrer
    redirect_url = "https://athena-publication.herokuapp.com/auth"
    link = "https://www.facebook.com/v14.0/dialog/oauth?" + "client_id=" + client_id + "&redirect_uri=" + redirect_url + "&state=" + state
    return redirect(link)

@app.route('/auth')
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
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
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)

@app.route('/dashboard/')
@login_required
def dashboard():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    all_collections = Collection.query.filter_by(creator_id=current_user.id).order_by(Collection.id.desc()).all()
    return render_template('dash.html', user=user, all_collections=all_collections)

