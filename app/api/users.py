from flask import jsonify, request, abort
from app.api import blueprint
from app.models import User
from app import db
from app.api.auth import token_auth
import app.api.errors as api_errors

@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if ('username' not in data) or ('email' not in data) or ('password' not in data):
        return api_errors.bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return api_errors.bad_request('username already taken')
    if User.query.filter_by(email=data['email']).first():
        return api_errors.bad_request('email already taken')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201

    return response
