from flask import (Flask, Markup, flash, jsonify, redirect, render_template,
                   request, send_file, url_for, session)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from tools import *
from werkzeug.datastructures import ImmutableMultiDict
from app import app, db
from app.models import (Collection, Media, User)
from .request import Collection_Request, Media_Request
from .process import ImageHandler
from .repo import Repo
import json
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


@app.route('/dashboard/')
@login_required
def dashboard():
    page  = request.args.get("page", 1, type=int)
    user = User.query.filter_by(id=current_user.id).first_or_404()
    all_collections = Collection.query.filter_by(creator_id=current_user.id).order_by(Collection.id.desc()).paginate(page=page,per_page=4, error_out = False)
    next_page = url_for("dashboard", page = all_collections.next_num) if all_collections.has_next else None
    prev_page = url_for("dashboard", page = all_collections.prev_num) if all_collections.has_prev else None
    return render_template('dash.html', user=user, all_collections=all_collections.items, next_page = next_page, prev_page = prev_page)

