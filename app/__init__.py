import argparse
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from app.helpers import deleting_folders_that_are_not_from_today
from app.routes import print_blueprint
from app.utils import delete_folder, print_ascii_art
from config import Config

load_dotenv()
PORT = os.getenv("PORT", 5000)  

app = Flask(__name__)
scheduler = APScheduler()
CORS(app)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 5000)), help="Port to run the Flask app")
args = parser.parse_args()
PORT = args.port 

scheduler.add_job(id='delete_old_folders', func=deleting_folders_that_are_not_from_today, trigger='cron', hour=1, minute=0)
scheduler.init_app(app)
scheduler.start()

print_ascii_art()
delete_folder('temp')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(print_blueprint)
    app.run(host='0.0.0.0', port=PORT, debug=True)

    return app
