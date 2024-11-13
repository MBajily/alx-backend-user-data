#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
auth = None


# Initialize authentication type based on environment variable
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()


@app.before_request
def before_request():
    """Assigns request.current_user if authenticated"""
    if auth is None:
        return
    request.current_user = auth.current_user(request)


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
