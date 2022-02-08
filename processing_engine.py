import os
import pickle
import csv
import re
import glob
import string
import nltk
from nltk.corpus import stopwords
import pickle


class ProcessingEngine:
    ''' No longer doubles as a bad recommending engine '''

    def __init__(self, lang, verbose=1):
        print('Starting processing engine...')
        # self.job_descriptions = []

        # this should be in a config file, not inside the code
        self.verbose = verbose
        self.supported_languages = {
            'en': 'english'
        }
        if lang not in self.supported_languages:
            print('Language not supported, default to "en"')
        else:
            self.lang = lang

        self.load_stopwords()

    def load_stopwords(self):
        nltk.download('stopwords', quiet=True)  # this will probably mess stuff up
        self.stopwords = nltk.corpus.stopwords.words(self.supported_languages[self.lang])
    
    def load_keywords(self, file_path):
        print(f'{"Loading keywords":<50}', end='', flush=False)
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            keywords = []
            for row in reader:
                word = row[0]
                word = word.strip().lower()
                keywords.append(word)

        keywords = [k for k in keywords if len(k) > 1]
        self.keywords = keywords
        print('Done')

    def set_job_description(self, description):
        self.job_description = description

    def load_job_description(self, job_description: string, is_pickle: bool=True):
        if is_pickle:
            self.original_job_description = pickle.load(open(job_description, 'rb'))
        else:
            self.original_job_description = job_description

    def process_job_description(self):
        print(f'{"Processing job description":<50}', end='', flush=False)
        job = self.original_job_description.strip()
        job = job.translate(str.maketrans('', '', string.punctuation))  # remove punctiation (),.!
        
        pattern = re.compile(r'\b{}\b'.format(r'\b|\b'.join(self.stopwords)))  # remove stopwords from nltk module
        job = pattern.sub('', job)
        pattern_alphanumeric = re.compile('[\W_]+')
        job = pattern_alphanumeric.sub(' ', job)

        self.job_description = job
        self.keywords = [word for word in job.split()]
        print('Done')
        return self.job_description

    def load_resumes(self, resumes: string, is_pickle: bool=True):
        if is_pickle:
            self.original_resumes = pickle.load(open(resumes, 'rb'))
        else:
            self.original_resumes = resumes

    def process_resumes(self):
        print(f'{"Processing resumes":<50}')
        self.processed_resumes = []
        for file_path, resume in self.original_resumes:
            file_name = file_path.split('\\')[-1]
            print(f'\t{file_name}')
            resume = resume.strip()
            resume = resume.translate(str.maketrans('', '', string.punctuation))  # remove punctuation (),.!
            
            pattern = re.compile(r'\b{}\b'.format(r'\b|\b'.join(self.stopwords)))  # remove stopwords from nltk module
            resume = pattern.sub('', resume)

            self.processed_resumes.append((file_path, resume))

        return self.processed_resumes

    def run_engine(self):  # combined methods
        job_description = self.process_job_description()
        resumes = self.process_resumes()

        return job_description, resumes
        

    # pickle for debugging
    def pickle_job_description(self, pickle_name='processed_job_description'):
        print(f'{"Saving processed job description":<50}', end='', flush=False)
        output_filename = os.path.join('pickle_dev', pickle_name + '.pickle')
        with open(output_filename, 'wb') as output_file:
            pickle.dump(self.job_description, output_file)

        print(f'"{output_filename}"')

    def pickle_resumes(self, pickle_name='processed_resumes'):
        print(f'{"Saving processed resumes":<50}', end='', flush=False)
        output_filename = os.path.join('pickle_dev', pickle_name + '.pickle')
        with open(output_filename, 'wb') as output_file:
            pickle.dump(self.processed_resumes, output_file)

        print(f'"{output_filename}"')

if __name__ == '__main__':
    job_description_path = os.path.join('pickle_dev', 'ingested_job_description.pickle')
    resume_path = os.path.join('pickle_dev', 'ingested_resumes.pickle')

    processing_engine = ProcessingEngine('en')  # class instance
    
    
    # load from pickle
    # processing_engine.load_keywords(en_keywords_path)  # keywords
    processing_engine.load_job_description(job_description_path, is_pickle=True)
    processing_engine.load_resumes(resume_path, is_pickle=True)
    
    # process stuff
    job_description = processing_engine.process_job_description()
    resumes = processing_engine.process_resumes()

    # pickle for dev
    processing_engine.pickle_job_description()
    processing_engine.pickle_resumes()
