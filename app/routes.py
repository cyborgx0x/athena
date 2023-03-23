from flask import (jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from app import app

@app.get("/privacy-policy")
def privacy():
    return jsonify(dict(
        detail="Privacy Policy"
    )),200

@app.get("/TOS")
def tos():
    return jsonify(dict(
        detail="TOS"
    )),200
