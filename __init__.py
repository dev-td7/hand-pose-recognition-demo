from flask import Flask
import os

app = Flask(__name__)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha'

app.config.from_object(Config)
from app import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0')
