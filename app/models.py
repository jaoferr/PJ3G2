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
from app import db, login
from app import document_db
from datetime import datetime, timedelta
from time import time
from flask import url_for
import os
import hashlib
import json
import base64
import werkzeug.security as security

class Resume(document_db.DynamicDocument):
    content = document_db.StringField(required=True)

class ResumeIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    resume_id = db.Column(db.String, index=True, unique=True)  # mongodb id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    filename = db.Column(db.String)
    batch_id = db.Column(db.String)

    def __repr__(self):
        return f'<Resume {self.id}, {self.filename}>'

    def from_dict(self, data: dict):
        for field in ['resume_id', 'user_id', 'filename', 'batch_id']:
            if field in data:
                setattr(self, field, data[field])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    def get_token(self, expires_in: int=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token: str):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        
        return user

    # def launch_task(self, name: str, description: str, *args, **kwargs):
    #     kwargs['locale'] = g.locale
    #     rq_job = current_app.task_queue.enqueue('app.tasks.' + name, self.id, *args, **kwargs)
    #     task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
    #     db.session.add(task)
    #     return task

    # def get_tasks_in_progress(self):
    #     return Task.query.filter_by(user=self, complete=False).all()

    # def get_task_in_progress(self, name):
    #     return Task.query.filter_by(name=name, user=self, complete=False).first()

    # def to_dict(self, include_email=False):
    #     data = {
    #         'id': self.id,
    #         'username': self.username,
    #         'last_seen': self.last_seen.isoformat() + 'Z',
    #         'about_me': self.about_me,
    #         'post_count': self.posts.count(),
    #         'follower_count': self.followers.count(),
    #         'followed_count': self.followed.count(),
    #         '_links': {
    #             'self': url_for('api.get_user', id=self.id),
    #             'followers': url_for('api.get_user_followers', id=self.id),
    #             'followed': url_for('api.get_user_followed', id=self.id),
    #             'avatar': self.avatar(128)
    #         }
    #     }
    #     if include_email:
    #         data['email'] = self.email
        
    #     return data

    # def from_dict(self, data, new_user=False):
    #     for field in ['username', 'email', 'about_me']:
    #         if field in data:
    #             setattr(self, field, data[field])
    #     if new_user and 'password' in data:
    #         self.set_password(data['password'])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))