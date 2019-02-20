from flask import Flask
from app.instance.config import *
from flask_oauth import OAuth

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

from app.routes import routes,google_authentication

def main():
    app.run(debug=True)

main()
