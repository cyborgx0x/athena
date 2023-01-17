'''
should contain modules that process data from the request so the service can work with

'''
import requests
import base64

class ImageHandler():
    def __init__(self, source) -> None:
        self.source = source
    def upload(self):
        data = {
            "image": base64.b64encode(self.source.read()).decode()
        }
        api = "b4efdd223b0240f2b1212a0cef3bda37"
        link = "https://api.imgbb.com/1/upload?key="
        response = requests.post(link+api, data=data)
        print(response.status_code)
        if response.status_code == 200:
            print(response.text)
            self.url = response.json()["data"]["image"]["url"]
            
            self.upload_status = True
        else:
            self.url = ""
            self.upload_status = False