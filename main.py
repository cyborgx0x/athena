from app.models import Collection, User
from app import app, db


@app.shell_context_processor
def make_shell_context():
    return {'db': db, "Collection": Collection, "User": User}

if __name__=="__main__":
    print("starting flask")
    app.run()