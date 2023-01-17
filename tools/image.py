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
