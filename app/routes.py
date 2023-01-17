import json, os
from flask import (Flask, Markup, flash, jsonify, redirect, render_template,
                   request, send_file, url_for, session)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from tools import *
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_parse
import requests
from app import app, db
from app.form import (LoginForm,
                      RegistrationForm)
from app.models import (Collection, Media, User)
from datetime import datetime
import urllib.parse
from .request import Collection_Request, Media_Request
from .process import ImageHandler
from .repo import Repo

@app.route("/")
def index():
    top_view_collections = Collection.query.filter_by(status="public").order_by(Collection.view.desc()).limit(20).all()
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
        res = upload(request.files["image"])
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
    if current_user.id == user.id or current_user.type == 1:
        if request.method == 'POST' and request.form:
            user.name = request.form.get("user_full_name")
            try:
                res =  upload(request.files["user_avatar"])
                user.avatar = res["data"]["image"]["url"]
            except requests.exceptions.JSONDecodeError as e:
                print(e.strerror)
            db.session.commit()
            return redirect(url_for("edit_user", id=id))
        elif request.method == "POST" and current_user.id  == user.id and request.data:
            incoming_data= json.loads(request.data.decode('UTF-8'))
            if incoming_data["type"] == "content":
                return jsonify(user.about_me)
            elif incoming_data["type"] == "upload":
                user.about_me =incoming_data["value"]
                db.session.commit()
                return "success 🔥🔥🔥"
        return render_template("edit_user.html", user = user)
    else:
        return redirect(url_for("index"))


@app.route("/all_collections")
def all_collections():
    page = request.args.get("page", 1, type=int)
    all_collections = Collection.query.filter_by(status="public").order_by(Collection.name.desc()).paginate(page=page)
    next_page = url_for("all_collections", page = all_collections.next_num) if all_collections.has_next else None
    prev_page = url_for("all_collections", page = all_collections.prev_num) if all_collections.has_prev else None
    return  render_template("all_collections.html", all_collections = all_collections.items, title =  "Tất cả tác phẩm", next_page = next_page, prev_page = prev_page)


@app.route("/collection/<int:id>/", methods=['GET', 'POST'])
def public_collection(id):
    
    collection = Collection.query.filter_by(id=id).first()
    if collection.view == None:
        collection.view = 1
        db.session.commit()
    else:
        collection.view += 1
        db.session.commit()
    
    return  render_template("public_collection.html", collection = collection)

@app.route("/user/<id>")
def user_profile(id):
    page = request.args.get("page", 1, type=int)
    all_collections = Collection.query.filter_by(creator_id = id, status = "public").paginate(page=page)
    user = User.query.filter_by(id = id).first()
    next_page = url_for("user_profile", id=id, page = all_collections.next_num) if all_collections.has_next else None
    prev_page = url_for("user_profile", id=id, page = all_collections.prev_num) if all_collections.has_prev else None
 
    return render_template("user.html", collections = all_collections.items, user = user, next_page=next_page, prev_page=prev_page)


@app.route("/tag/<tag>")
def tag_view(tag):
    collections = Collection.query.filter(Collection.tag.like("%" + tag + "%"))
    return render_template("all_collections.html", all_collections = collections, title = tag +  ": Tất cả tác phẩm")

@app.route("/edit/collection/<int:id>/", methods=['GET', 'POST'])
@login_required
def edit_collection(id):
    collection = Collection.query.filter_by(id=id).first()
    if current_user.id == collection.creator_id or current_user.type == 1:
        if request.method == 'POST' and request.form:
            request_handle = Collection_Request()
            if request_handle.populate(request.form):
                if request.files:
                    image = ImageHandler(request.files["book-cover"])
                    request_handle.image = image
                    request_handle.image_upload()
                repo = Repo(db=db, model=collection)
                repo.save(request_handle)
            return redirect(url_for('edit_collection', id=id))
        elif request.method == "POST" and request.data:
            request_handle = Collection_Request()
            if request_handle.byte_handle(request=request.data):
                repo = Repo(db=db, model=collection)
                status = repo.save(request_handle)
                return jsonify(status)
        return  render_template("edit_collection.html", collection = collection)
    else:
        return  redirect(url_for("index"))

@app.route("/api/collection/<int:id>/")
@login_required
def collection_content(id):
    collection = Collection.query.filter_by(id=id).first()
    return jsonify(collection.desc)


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
    if current_user.id == chapter.user_id or current_user.type == 1:
        if request.method == 'POST' and request.data:

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
    print(request.args)
    type = request.args.get("type")
    id = request.args.get("id")
    if type == "collection":
        col = Collection.query.filter_by(id = id).first()
        if current_user.id == col.creator_id or current_user.type == 1:
            Media.query.filter_by(collection_id = id).delete()
            Collection.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)
    elif type == "media":
        media = Media.query.filter_by(id=id).first()
        if current_user.id == media.user_id or current_user.type == 1:
            Media.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)


'''
User Session
Contain route about user authentication, profile, configuration and dashboard
'''

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
    page  = request.args.get("page", 1, type=int)
    user = User.query.filter_by(id=current_user.id).first_or_404()
    all_collections = Collection.query.filter_by(creator_id=current_user.id).order_by(Collection.id.desc()).paginate(page=page)
    next_page = url_for("dashboard", page = all_collections.next_num) if all_collections.has_next else None
    prev_page = url_for("dashboard", page = all_collections.prev_num) if all_collections.has_prev else None
 
    return render_template('dash.html', user=user, all_collections=all_collections.items, next_page = next_page, prev_page = prev_page)

