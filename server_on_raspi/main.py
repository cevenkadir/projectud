from flask import Flask, request, jsonify

import socket, os

app = Flask(__name__)
#os.environ.get('AUTH_KEY')
@app.route('/', methods=['GET'])
def check_status():
    return jsonify({'status': True})



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)