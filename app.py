from ingesting_engine import IngestingEngine
from processing_engine import ProcessingEngine
import os
import pickle
from pprint import pprint


if __name__ == '__main__':
    # ingest folder with multiple resumes
    folder = os.path.join('Original_Resumes', '')
    ingesting_engine = IngestingEngine(verbose=1)
    # data = ingesting_engine.process_folder(folder)
    # ingesting_engine.pickle_texts()

    # process and recommend
    folder_path = './Job_Description/'
    job_description_path = './Job_Description/oaktree.txt'
    en_keywords_path = 'keywords/en_keywords_fixed.csv'

    # dev
    data_path = open('ingested.pickle', 'rb')
    data = pickle.load(data_path)

    processing_engine = ProcessingEngine()  # class instance
    processing_engine.load_keywords(en_keywords_path)  # keywords
    processing_engine.load_job_description(job_description_path)  # job desc
    processing_engine.load_resumes(data)  # data = texts from ingesting engine
    processing_engine.match_keywords()  # loop through all resumes and get their scores
    k = processing_engine.get_best_resumes()  # return best scores
