# from app.models import Collection, User
from app import app
from auth.auth import auth_bp
from fiction.app import fiction
from asset.app import asset
from chapter.app import chapter
from flask_login import LoginManager

app.register_blueprint(auth_bp)
app.register_blueprint(fiction)
app.register_blueprint(asset)
app.register_blueprint(chapter)

login = LoginManager(app)
login.login_view = 'auth_bp.login'

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, "Collection": Collection, "User": User}

if __name__=="__main__":
    print("starting flask")
    app.run()