from flask import jsonify, request
from app.api import blueprint
from app.api.auth import token_auth
from app.models import Resume, ResumeIndex
from app import db
from bson.objectid import ObjectId
from hashlib import md5

import app.api.errors as api_errors

# @blueprint.route('/documents/<document_hash:str>', methods=['GET'])
def documents(hash: str):
    pass

@blueprint.route('/resumes', methods=['GET'])
@token_auth.login_required
def get_resume():
    object_id = request.args.get('resume_id', type=str)
    print(object_id)
    if not object_id:
        return api_errors.bad_request('request must have an object_id')
    
    result = Resume.objects(_id=ObjectId(object_id))[0]
    return jsonify(result)


@blueprint.route('/resumes', methods=['POST'])
@token_auth.login_required
def insert_resume():
    data = request.get_json() or {}
    if 'content' not in data:
        return api_errors.bad_request('content must not be none')

    new_resume = Resume(content=data['content'])
    new_resume.save()

    if new_resume.id:
        resume_id = str(new_resume.id)
        response = jsonify({
            'success': True,
            'object_id': resume_id
        })

        current_user = 0  # placeholder
        filename = 'path/to/file'  # placeholder
        batch_id = md5('placeholder'.encode('utf-8')).hexdigest()  # placeholder
        resume = ResumeIndex(
            resume_id=resume_id,
            user_id=current_user,
            filename=filename,
            batch_id=batch_id
        )
        db.session.add(resume)
        db.session.commit()
    else:
        response = jsonify({
            'success': False
        })

    return response
