import os
from tika import tika, parser
from zipfile import ZipFile
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage, FileMultiDict

class ResumeFile(object):
    ''' represents an uploaded resume file '''


class IngestingEngine:

    @staticmethod
    def process_file_tika(filename):
        ''' Process PDF file with tika '''
        parsed_pdf = parser.from_file(filename)
        data = parsed_pdf['content']
        return data

    def __init__(self):
        self.parsing_methods = {
            'tika_default': IngestingEngine.process_file_tika
        }
        self.default_parsing_method = self.parsing_methods['tika_default']

    def init_app(self, app):
        if 'TIKA_SERVER_ENDPOINT' not in app.config:
            print(f'Tika server is not running. Using self contained server.')
        else:
            self.tika_server_endpoint = app.config['TIKA_SERVER_ENDPOINT']

        self.allowed_extensions = app.config['INGESTING_ALLOWED_EXTENSIONS']

    def is_file_allowed(self, filename: str):
        return '.' in filename and filename.split('.')[-1].lower() in self.ALLOWED_EXTENSIONS

    def scan_zip_file(self, file_object: FileStorage):
        '''
        opens zip file in-memory
        adds each one to self.files
        '''
        zip_object = ZipFile(file_object)
        files = {}

    def process_files(self, parsing_method_name: str=None) -> list[tuple]:
        texts = []
        parsing_method = self.parsing_methods[parsing_method_name] or self.default_parsing_method
        for file in self.files:
            if self.verbose != 0:
                file_name = file.split('\\')[-1]
                print(f'Parsing file: {file_name}')
            parsed_file = parsing_method(file)                               # ex: pdf = tika
            # simple cleaning
            parsed_file = parsed_file.lower().replace('\n', '').strip()
            texts.append((file, parsed_file))

        return texts

    def insert_to_db(self):
        pass

    def run_task(self, file_obj):
        pass
