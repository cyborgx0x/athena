import json
import re

from flask import (Flask, Markup, flash, jsonify, redirect, render_template,
                   request, send_file, url_for, session)
from flask_login import current_user, login_required, login_user, logout_user
from tools import *
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_parse
import ast
import requests
from app import app, db
from app.form import (LoginForm,
                      RegistrationForm)
from app.models import (Collection, Media, User, UserAction, CollectionAction, MediaAction)
from datetime import datetime

@app.route("/")
def index():
    top_view_collections = Collection.query.filter_by(status="public").limit(20).all()
    top_creators = User.query.limit(12).all()
    return  render_template("home.html", top_view_collections = top_view_collections, top_creators=top_creators)


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
    url="http://skybooks.vn/wp-content/uploads/2021/03/chung-ta-khong-the-la-ban-tang-kem-bookmark-so-tay-1.jpg"
    print(link)
    img = return_img(link)
    img.seek(0)
    return  send_file(img, mimetype='image/jpeg')


@app.route("/creator/<id>", methods=['GET', 'POST'])
def view_creator(id):
    user = User.query.filter_by(id=id).first()
    collections = Collection.query.filter_by(creator_id=user.id, status="public")
    return render_template("public_user.html", user = user, collections =collections)

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

@app.route("/creators/")
def all_creators():
    users = User.query.all()
    top_users = User.query.limit(12).all()
    return render_template("all_users.html", users = users, top_users=top_users, title="Người sáng tạo")

@app.route("/following/")
def following_user():
    following = User.query.join(User.affected).filter_by(user_id=current_user.id)
    return render_template("all_users.html", users = following, title="Following")

@app.route("/all_collections")
def all_collections():
    all_collections = Collection.query.filter_by(status="public")
    return  render_template("all_collections.html", all_collections = all_collections, title =  "Tất cả tác phẩm")

@app.route("/liked/")
def liked_collection():
    collections = CollectionAction.query.filter_by(user_id=current_user.id, type="userlove")
    return  render_template("all_collections.html", collections = collections)


@app.route("/collection/<int:id>/", methods=['GET', 'POST'])
def public_collection(id):
    collection = Collection.query.filter_by(id=id).first()
    return  render_template("public_collection.html", collection = collection)

@app.route("/author/<author_name>")
def author_viewẻ(author_name):
    collections = Collection.query.filter_by(author = author_name)
    return render_template("all_collections.html", all_collections = collections, title = author_name +  ": Tất cả tác phẩm")


@app.route("/edit/collection/<int:id>/", methods=['GET', 'POST'])
@login_required
def edit_collection(id):
    collection = Collection.query.filter_by(id=id).first()
    if request.method == 'POST':
       
        incoming_data= json.loads(request.data.decode('UTF-8'))
        print(json.dumps(incoming_data))
        if incoming_data["type"] == "content":
            return jsonify(collection.desc)
        elif incoming_data["type"] == "upload":
            try: 
                collection.desc = incoming_data["value"]
                print(collection.desc)
                db.session.commit()
                return "Đã cập nhật lời tựa"
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
        elif incoming_data["type"] == "collection-status":
            collection.status = incoming_data["value"]
            db.session.commit()
            if collection.status == "public":
                return "Đã thay đổi trạng thái thành: Công khai"
            else:
                return "Đã trở về bản nháp"
    print(current_user.id, collection.creator_id)
    if current_user.id == collection.creator_id:
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
    chapters = Media.query.filter_by(collection_id=collection.id)
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
    if current_user.id == chapter.user_id:
        return render_template('edit_media.html', chapter=chapter)
    else:
        return redirect(url_for("dashboard"))




'''
API SESSION
Contain interaction with the request from client
'''

@app.route ("/api/bookmark/", methods=['POST'])
def bookmark_api():
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        if incoming_data['value'] == "remove":
            item = MediaAction.query.filter_by(media_id=incoming_data['chapter'], user_id=current_user.id, type="mediabookmark").delete()
            db.session.commit()
            return "remove bookmark successfully"
        else:
            newitem = MediaAction(user_id=current_user.id, media_id=incoming_data['chapter'], type="mediabookmark")
            db.session.add(newitem)
            db.session.commit()
            return "added bookmark successfully"
    return "message received"


@app.route("/editor/<int:collection_id>/new-chapter/", methods=['GET', 'POST'])
def new_chapter(collection_id):
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
    new_collection = Collection(name="Tác phẩm mới", status="draft", creator_id=current_user.id)
    db.session.add(new_collection)
    db.session.commit()
    db.session.refresh(new_collection)
    return redirect(url_for('edit_collection', id=new_collection.id))


@app.route("/user/love/",methods=['GET', 'POST'])
def update_love():
    love =  current_user.collectionaction
    data = [col for col in love]
    print(data)
    if request.method == 'POST':
        data= json.loads(request.data.decode('UTF-8'))
        print(data)
        if data['type'] == "love" and data['value'] == "love":
            love = CollectionAction(user_id = current_user.id, collection_id = data['id'], type="collection_love")
            db.session.add(love)
            db.session.commit()
            total_love = CollectionAction.query.filter_by(collection_id=data['id'], type="collection_love").count()
            return "has " + str(total_love) + " ❤"
        else:
            itemdelete = CollectionAction.query.filter_by(user_id=current_user.id,collection_id=data['id'],type="collection_love").delete()
            db.session.commit()
            total_love = CollectionAction.query.filter_by(collection_id=data['id'], type="collection_love").count()
            return "has " + str(total_love) + " ❤"
    return jsonify(data)


@app.route("/api/following/",methods=['GET', 'POST'])
def update_follower():
    string = " follower 🧑"
    if request.method == 'POST':
        data = json.loads(request.data.decode('UTF-8'))
        if data['type'] == "user-follow" and data['value'] == "follow":
            UserAction.query.filter_by(user_id=current_user.id,affected=int(data['user']), type="userfollow").delete()
            db.session.commit()
            
            follower = UserAction.query.filter_by(affected=int(data['user'])).count()
            return "<strong>" + str(follower) + string + "</strong>"
        elif data['type'] == "user-follow" and data['value'] == "followed":
            follower = UserAction(user_id=current_user.id, affected=int(data['user']), type="userfollow")
            db.session.add(follower)
            db.session.commit()
           
            follower = UserAction.query.filter_by(affected=int(data['user'])).count()
            return "<strong>" + str(follower) + string + "</strong>"
        elif data['type'] == "get-follow":
            f = []
            for user in current_user.do:
                f.append(user)
            return jsonify(f)
    return "no input"



'''
DANGER SESSION
contain link and API for delete item
must control it with carefully behaviour
'''

@app.route("/collection/<int:id>/delete", methods=['GET', 'POST'])
def delete_collection(id):
    MediaAction.query.join(Media.collection).filter_by(id=id).delete()
    CollectionAction.query.filter_by(collection_id=id).delete()
    Media.query.filter_by(collection=id).delete()
    Collection.query.filter_by(id=id).delete()
    db.session.commit()
    return  redirect(url_for("dashboard"))

@app.route("/media/<int:id>/delete", methods=['GET', 'POST'])
def delete_chapter(id):
    media = Media.query.filter_by(id=id).first()
    next = url_for('edit_collection', id=media.collection_id)
    MediaAction.query.filter_by(media_id=id).delete()
    media = Media.query.filter_by(id=id).delete()
    db.session.commit()
    return  redirect(next)


'''
User Session
Contain route about user authentication, profile, configuration and dashboard
'''
@app.route('/authorized', methods=['GET','POST'])
def authorized():
    access_token = request.args.get("access_token")
    print(access_token)
    return redirect("/")


@app.route('/login', methods=['GET','POST'])
def login():
    code = request.args.get("access_token")
    print(code)
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
    if request.method == "POST":
        incoming_data = json.loads(request.data.decode('UTF-8'))
        incoming_data = incoming_data['data']
        core_url = "https://graph.facebook.com/v10.0/me?fields=id,name,email,picture{url}&access_token="
        access_token = incoming_data['authResponse']['accessToken']
        avatar_url = "https://graph.facebook.com/v10.0/me/picture?fields=url&width=480&access_token="
        auth = requests.get(core_url + access_token)
        print(auth)
        if auth.status_code == 200:
            r = json.loads(auth.text)
            id = r['id']
            name = r['name']
            email = r['email']
            avatar = r['picture']['data']['url']
            user = User.query.filter_by(facebook=id).first()
            if user is None:
                new_user = User(facebook=id, name=name, email=email)
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)
                login_user(new_user,duration=incoming_data['authResponse']['data_access_expiration_time'])
                return "added" 
            if user.email == None:
                user.email = email
            user.avatar = avatar
            user.last_seen = datetime.now() 
            db.session.commit()
            login_user(user,duration=incoming_data['authResponse']['data_access_expiration_time'])
            return "signed"
    return render_template('login.html', title='Sign In', form = form)
    
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
    all_collections = Collection.query.filter_by(creator_id=current_user.id)
    return render_template('dash.html', user=user, all_collections=all_collections)

