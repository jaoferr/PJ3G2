from app import create_app, db, document_db
from app.models import User, Resume, ResumeIndex

app = create_app()

@app.shell_context_processor
def make_shell_context():
    context = {
        'db': db,
        'mongodb': document_db,
        'user': User,
        'doc': Resume,
        'idoc': ResumeIndex
    }
    return context
