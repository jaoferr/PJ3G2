from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

from app.api.resources import resumes
api.add_resource(resumes, '/resumes/<int:id>')
