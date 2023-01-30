# from app.models import Collection, User
from app import app
from auth.auth import auth_bp
app.register_blueprint(auth_bp)


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, "Collection": Collection, "User": User}

if __name__=="__main__":
    print("starting flask")
    app.run()