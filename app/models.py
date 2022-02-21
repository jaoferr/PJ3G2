'''
Documents
    document_id     simple incremental id
    document_hash   hash from name + content
    user_id         user who added the document
    content         actual content from file, after ingestion from tika
    datetime        datetime when added
    filename        original filename
    description     optional description of document
    content_type    if resume or job description
    batch           batch id, used to work with files that were added together

User
    user_id         user_id, unique
    username        username
    email           email
    password        password
    token           token for access
    token_exp.      datetime of token expiration
    
    additional
        last_access
        datetime_created
        user_level

'''
from app import db
from datetime import datetime, timedelta
from time import time

import os
import hashlib
# import json
# import base64
# import werkzeug.security as security

# class Document(db.Model):
#     document_id = db.Column(
#         db.Integer, index=True, 
#         unique=True, primary_key=True, autoincrement=True
#     )
#     document_hash = db.Column(db.Binary(16), index=True, unique=True)
#     user_id = ''  # relationship w/ user?
#     content = db.Column()

''' maybe nosql? '''
