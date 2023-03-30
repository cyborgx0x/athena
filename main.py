# from app.models import Collection, User
from app import app
from app.chapter.app import chapter
from app.fiction.app import fiction
from app.auth.app import auth_bp
from app.asset.app import asset


app.register_blueprint(asset)
app.register_blueprint(auth_bp)
app.register_blueprint(fiction)
app.register_blueprint(chapter)

if __name__=="__main__":
    print("starting flask")
    app.run()   