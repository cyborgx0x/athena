import json
class Request(object):
    id = 1
    data = {
        "title": "old title"
    }

    title = "Title"
    def save(self, *args, **kwargs):
        for arg in args:
            print(json.loads(self))

req = Request()
print(req.save(*["id", "data"]))
