from app.models import Collection
from app import app, db


@app.shell_context_processor
def make_shell_context():
    return {'db': db, "Collection": Collection}

if __name__=="__main__":
    print("starting flask")
    app.run()