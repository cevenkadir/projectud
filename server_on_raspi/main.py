import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv

#Loading the .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
AUTH_KEY = os.environ.get('AUTH_KEY')

app = Flask(__name__)

#A function checking authorization key
def check_auth_key():
    try:
        req_data = request.get_json(force=True)
        auth_bool = req_data['auth_key'] == AUTH_KEY
    except:
        return False
    else:
        if auth_bool:
            return True
        else:
            return False

@app.route('/', methods=['GET', 'POST'])
def check_status():
    return jsonify({'status': check_auth_key()})

if __name__ == "__main__":
    app.run(host="0.0.0.0")