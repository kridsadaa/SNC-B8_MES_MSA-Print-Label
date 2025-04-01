import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from app.routes import print_blueprint
from app.utils import delete_folder, print_ascii_art, schedule_task
from config import Config

load_dotenv()
PORT = os.getenv("PORT", 5000)  
DEFAULT_PRINTER = os.getenv("DEFAULT_PRINTER", "mahingsa_printer")  

app = Flask(__name__)
CORS(app)

def create_app():
    print_ascii_art()
    delete_folder('temp')
    schedule_task(delete_folder, '00:00', 'temp') 
       
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(print_blueprint)

    
    app.run(host='0.0.0.0', port=PORT, debug=True)

    return app
