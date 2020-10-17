import os

from flask import Flask
from settings import root_service

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "system maintenance"


@app.route('/restart', methods=['GET'])
def restart_gateway():
    os.popen("bash restart.sh")
    print("------------------------> gateway restart")
    return {"code": 0}


if __name__ == '__main__':
    app.run(host=root_service['host'], port=root_service['port'])
