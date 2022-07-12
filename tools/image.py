import requests
from PIL import Image, ImageOps
import io
import numpy as np
import base64

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

if __name__ =="__main__":
    img = return_img('http://skybooks.vn/wp-content/uploads/2021/03/Bia-Yeu-quai-nho-1.png')
    print(img)

def upload(source):
    data = {
        "image": base64.b64encode(source.read()).decode()
    }
    api = "b4efdd223b0240f2b1212a0cef3bda37"
    link = "https://api.imgbb.com/1/upload?key="
    response = requests.post(link+api, data=data)
    return response.json()