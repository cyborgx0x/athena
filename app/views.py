from flask.views import View, MethodView
from flask import jsonify, request
from app import db
from flask_praetorian import auth_required

class ItemAPIView(MethodView):
    decorators = [auth_required]
    init_every_request = False

    def __init__(self, model):
        self.model = model
        # self.validator = generate_validator(model)

    def _get_item(self, id):
        return self.model.query.get_or_404(id)

    def get(self, id):
        item = self._get_item(id)
        return jsonify(item.to_json())

    def patch(self, id):
        item = self._get_item(id)
        # errors = self.validator.validate(item, request.json)

        # if errors:
        #     return jsonify(errors), 400

        item.update_from_json(request.json)
        db.session.commit()
        return jsonify(item.to_json())

    def delete(self, id):
        item = self._get_item(id)
        db.session.delete(item)
        db.session.commit()
        return "", 204


class ListCreateAPIView(MethodView):
    init_every_request = False
    decorators = [auth_required]
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


def register_api(app, model, name):
    item = ItemAPIView.as_view(f"{name}-item", model)
    group = ListCreateAPIView.as_view(f"{name}-group", model)
    app.add_url_rule(f"/{name}/<uuid:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)

