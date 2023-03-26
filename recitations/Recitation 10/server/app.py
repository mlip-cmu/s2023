""" Implements a flask server the responds with the current time"""
from flask import Flask
from datetime import datetime
import os


app = Flask(__name__)


@app.route('/')
def home():
    """ Returns the index page"""
    return """<center>
    <h1>Welcome to Recitation 10: Container Orchestration with Kubernetes</h1>
    <h3>Kubernetes is an open-source container orchestration system for automating software deployment, scaling, and management.
    Originally designed by Google, the project is now maintained by the Cloud Native Computing Foundation. 
    The name Kubernetes originates from Greek, meaning 'helmsman' or 'pilot'.
    </h3>
    </center>"""


@app.route('/datetime')
def get_datetime():
    """ Returns the current time"""
    return f"The current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


@app.route('/health/<req>', methods=['GET'])
def health(req):
    """ Returns the health of the server"""
    if req == "kill":
        print("Killing server...")
        os._exit(0)
    else:
        return "Healthy"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
