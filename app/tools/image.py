import requests
from PIL import Image, ImageOps
import io
import numpy as np
import base64
import requests
import os

def getimage(link):
    image = requests.get(link)
    return io.BytesIO(image.content)

def resizecrop(src, width, height):
    img = Image.open(src)
    img = ImageOps.fit(img, (width, height), Image.ANTIALIAS, 0, (0.5, 0.5))
    c=io.BytesIO()
    try: 
        img.save(c, format='jpeg')
    except:
        img.save(c, format='png')
    return c

def return_img(link):
    response = getimage(link)
    img = resizecrop(response, 450, 720)
    return img

class ImageHandler():
    @staticmethod
    def upload_to_imgbb(source) -> str:
        data = dict(
            image=base64.b64encode(source.read()).decode()
        )
        api = os.getenv("IMAGE_KEY")
        link = "https://api.imgbb.com/1/upload?key="
        response = requests.post(f"{link}{api}", data=data)
        if response.status_code == 200:
            url = response.json()["data"]["image"]["url"]
            return url
        else:
            raise ConnectionError("Error when Upload Image, Please Try Again")