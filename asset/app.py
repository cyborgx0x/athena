from flask import Blueprint, request, send_file
from tools.image import ImageHandler, return_img, getimage
import json


asset = Blueprint("asset", __name__, template_folder="templates", static_folder='static')



@asset.get("/image_proxy/")
def img_proxy():
    link = request.args.get("image_url")
    img = return_img(link)
    img.seek(0)
    return  send_file(img, mimetype='image/jpeg')

@asset.route("/upload_link",methods = ['POST'])
def upload_image_by_link():
    if request.method == "POST":
        link = json.loads(request.data.decode("UTF-8"))["url"]
        file  = getimage(link)
        return ImageHandler.upload_to_imgbb(file)

@asset.route("/upload_image",methods = ['POST'])
def upload_image():
    if request.method == "POST":
        return ImageHandler.upload_to_imgbb(request.files["image"])