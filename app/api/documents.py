from flask import jsonify, request, url_for, abort
from app.api import blueprint
# from app.models
from app import db
from app.api.auth import token_auth

import app.api.errors as api_errors

@blueprint.route('/documents/<document_hash:str>', methods=['GET'])
def documents(hash: str):
    pass
