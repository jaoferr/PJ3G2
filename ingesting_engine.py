import glob
import os
from tika import parser
import time
import pickle


class IngestingEngine:

    @staticmethod
    def process_file_tika(filename):
        ''' Process pdf file with tika '''
        parsed_pdf = parser.from_file(filename)
        data = parsed_pdf['content']
        return data

    def __init__(self, extension=False, verbose=0):
        self.verbose = verbose  # controls log output
        self.supported_extensions = {
            'pdf': IngestingEngine.process_file_tika
        }

        if not extension:
            print('Starting engine, using default file extension (.pdf).')
            self.file_extension = 'pdf'
        elif extension not in self.supported_extensions.keys():
            raise ValueError(f'Extension {extension} is not supported.')
        else:
            print(f'Starting engine, using "{extension}" as file extension.')
            self.file_extension = extension.lower().strip()

        self.files = []

    def set_file_extension(self, extension):
        self.file_extension = extension

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
                print(f'Parsing file: {file}')
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

    def pickle_texts(self, pickle_name='ingested'):
        output_filename = pickle_name + '.pickle'
        with open(output_filename, 'wb') as output_file:
            pickle.dump(self.texts, output_file)

        print(f'Output save as pickle: "{output_filename}"')


if __name__ == '__main__':
    folder = os.path.join('Original_Resumes', '')
    ingesting_engine = IngestingEngine(verbose=1)
    data = ingesting_engine.process_folder(folder)
    ingesting_engine.pickle_texts()
