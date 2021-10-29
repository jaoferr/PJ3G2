import pickle
import csv
import re
import glob


class ProcessingEngine:
    ''' Also doubles as a bad recommending engine '''

    def __init__(self):
        print('\nStarting processing engine...')
        self.job_descriptions = []

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

    def load_job_description(self, file):
        print(f'{"Loading job description":<50}', end='', flush=False)
        with open(file, 'r', encoding='utf-8') as f:
            job = ''
            for row in f.readlines():
                string = row.strip().lower()
                job += ' ' + string

        job = job.strip()
        self.job_description = job
        self.job_descriptions.append(job)
        print('Done')

    def load_job_descriptions(self, folder_path):
        '''
        Receives a folder path with multiple text files,
        each with a job description
        currently not in use
        '''
        files = glob.glob(folder_path + '/*.txt')
        jobs = []
        for file in files:
            job = self.load_job_description(file)

    def load_resumes(self, resumes):
        # for now, we pickle
        self.resumes = resumes

    def build_pattern(self):
        print(f'{"Building patterns":<50}', end='', flush=False)
        sorted_keywords = sorted(self.keywords, key=len, reverse=True)
        pattern = re.compile('(?:\b{}\b)'.format('|'.join(map(re.escape, sorted_keywords))))
        self.pattern = pattern
        print('Done')

    def match_keywords(self):
        self.build_pattern()
        print(f'\n{"Matching":<50}', end='', flush=False)
        resume_matches = []
        for resume_path, resume in self.resumes:
            matches = self.pattern.findall(resume)
            resume_matches.append((resume_path, matches))

        self.matches = resume_matches
        print('Done')
        return resume_matches

    def get_best_resumes(self):
        resume_score = []
        for path, match in self.matches:
            resume_score.append((path, len(match)))

        resume_score.sort(key=lambda tup: tup[1], reverse=True)
        print(f'\nBest match is: {resume_score[0][0]} with {resume_score[0][1]} matches')
        print('\nOther matches:')
        for match in resume_score[1:]:
            print(f'\t{match[1]}: {match[0]}')
        return resume_score

# if __name__ == '__main__':
#     folder_path = './Job_Description/'
#     job_description_path = './Job_Description/oaktree.txt'
#     en_keywords_path = 'keywords/en_keywords_fixed.csv'

#     processing_engine = ProcessingEngine()  # class instance
#     processing_engine.load_keywords(en_keywords_path)  # keywords
#     processing_engine.load_job_description(job_description_path)
#     processing_engine.load_resumes(data)
#     processing_engine.match_keywords()
#     k = processing_engine.get_best_resumes()