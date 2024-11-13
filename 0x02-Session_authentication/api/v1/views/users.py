#!/usr/bin/env python3
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_authenticated_user():
    """Returns the authenticated user's data"""
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_dict())
