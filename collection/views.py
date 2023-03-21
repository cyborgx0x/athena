from flask.views import View, MethodView
from flask import jsonify, request
from app import db
class CollectionAPIView(View):

    init_every_request = False

    def __init__(self, model):
        self.model = model

    def dispatch_request(self):
        items = self.model.query.all()
        return jsonify(items)
    
class CollectionListAPIView(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        # self.validator = generate_validator(model, create=True)

    def get(self):
        items = self.model.query.all()
        return jsonify([item.to_json() for item in items])

    def post(self):
        # errors = self.validator.validate(request.json)

        # if errors:
        #     return jsonify(errors), 400
        item = self.model.from_json(request.json)
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_json())

