from flask_restful import Resource, reqparse
from app.api.auth import token_auth

class Resumes(Resource):
    method_decorators = {'post': [token_auth.login_required]}

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument()

        super(Resumes, self).__init__()

    def get(self):
        pass

    def post(self):
        pass

