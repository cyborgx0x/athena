import requests
import base64
from tools import *


def upload(source):
    data = {
        "image": base64.b64encode(source.getvalue()).decode()
    }
    api = "b4efdd223b0240f2b1212a0cef3bda37"
    link = "https://api.imgbb.com/1/upload?key="
    response = requests.post(link+api, data=data)
    return response.json()

img = return_img('http://skybooks.vn/wp-content/uploads/2021/03/Bia-Yeu-quai-nho-1.png')
print(upload(img))