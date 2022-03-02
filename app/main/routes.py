from app.main import blueprint
from flask import jsonify


@blueprint.route('/', methods=['GET'])
def index():
    return jsonify({
        'success': True
    })
