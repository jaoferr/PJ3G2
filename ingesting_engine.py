import glob
import os
from tika import tika, parser
import time
import pickle
import urllib.request


class IngestingEngine:

    @staticmethod
    def process_file_tika(filename):
        ''' Process PDF file with tika '''
        parsed_pdf = parser.from_file(filename)
        data = parsed_pdf['content']
        return data

    def __init__(self, extension=False, verbose=0, use_tika_server: bool=True, tika_server_endpoint: str='http://localhost:9998'):
        self.verbose = verbose  # controls log output
        self.supported_extensions = {
            'pdf': IngestingEngine.process_file_tika
        }
        if use_tika_server:
            try:
                tika_endpoint_status = urllib.request.urlopen(tika_server_endpoint).status
            except:
                tika_endpoint_status = 404

            if tika_endpoint_status == 200:
                tika.TIKA_SERVER_ENDPOINT = tika_server_endpoint
                print(f'Using Tika server at endpoint "{tika_server_endpoint}".')
            else:
                print(f'Tika server is not running at endpoint "{tika_server_endpoint}". Using self contained server.')

        if not extension:
            print('Starting ingesting engine, using default file extension (.pdf).')
            self.file_extension = 'pdf'
        elif extension not in self.supported_extensions.keys():
            raise ValueError(f'Extension {extension} is not supported.')
        else:
            print(f'Starting ingesting engine, using "{extension}" as file extension.')
            self.file_extension = extension.lower().strip()

        self.files = []

    def set_file_extension(self, extension):
        self.file_extension = extension

    # resumes
    def scan_folder(self, folder):
        '''
        Scans given folder for files with current extension
        and adds to file list
        '''
        print(f'Target folder: {folder}\n')
        folder_path = os.path.join(folder, '**', '*.' + self.file_extension)
        files = glob.glob(folder_path, recursive=True)

        self.files += files

    def process_files(self):
        texts = []
        for file in self.files:
            if self.verbose != 0:
                file_name = file.split('\\')[-1]
                print(f'Parsing file: {file_name}')
            parsing_method = self.supported_extensions[self.file_extension]  # pega o metodo p/ processamento
            parsed_file = parsing_method(file)                               # ex: pdf = tika
            # simple cleaning
            parsed_file = parsed_file.lower().replace('\n', '').strip()
            texts.append((file, parsed_file))

        return texts

    def process_folder(self, folder):
        ''' Processes entire folder and subfolders for current file extension '''
        start_timer = time.time()

        self.scan_folder(folder)
        texts = self.process_files()

        end_time = round(time.time() - start_timer, 3)
        print(f'\nDone parsing in {end_time}s')
        self.texts = texts
        return texts

    def pickle_resumes(self, pickle_name='ingested_resumes'):
        print(f'{"Saving ingested resumes":<50}', end='', flush=False)
        output_filename = os.path.join('pickle_dev', pickle_name + '.pickle')
        with open(output_filename, 'wb') as output_file:
            pickle.dump(self.texts, output_file)

        print(f'"{output_filename}"')

    # job description
    def load_job_description(self, file):
        print(f'{"Loading job description":<50}', end='', flush=False)
        with open(file, 'r', encoding='utf-8') as f:
            job = ''
            for row in f.readlines():
                string = row.strip().lower()
                job += ' ' + string

        self.original_job_description = job
        print('Done')
        return job

    def pickle_job_description(self, pickle_name='ingested_job_description'):
        print(f'{"Saving ingested job description":<50}', end='', flush=False)        
        output_filename = os.path.join('pickle_dev', pickle_name + '.pickle')
        with open(output_filename, 'wb') as output_file:
            pickle.dump(self.original_job_description, output_file)

        print(f'"{output_filename}"')

if __name__ == '__main__':
    folder = os.path.join('..', 'Resume&Job_Description', 'Original_Resumes')
    ingesting_engine = IngestingEngine(verbose=1, use_tika_server=True)
    resumes = ingesting_engine.process_folder(folder)
    job_description_path = os.path.join('..', 'Resume&Job_Description', 'Job_Description', 'oaktree.txt')
    job_description = ingesting_engine.load_job_description(job_description_path)
    
    # pickles
    ingesting_engine.pickle_resumes()
    ingesting_engine.pickle_job_description()
