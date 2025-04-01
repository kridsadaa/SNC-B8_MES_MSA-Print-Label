import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from app.routes import print_blueprint
from app.utils import delete_folder, print_ascii_art, schedule_task
from config import Config

load_dotenv()
PORT = os.getenv("PORT", 5000)  

app = Flask(__name__)
CORS(app)

def create_app():
    print_ascii_art()
    delete_folder('temp')
    folder_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")    
    folder = os.path.join("temp", folder_date)
    schedule_task(delete_folder, '01:00', folder) 
       
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(print_blueprint)
    app.run(host='0.0.0.0', port=PORT, debug=True)

    return app
