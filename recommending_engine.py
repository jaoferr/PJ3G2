import pickle
import nltk
import nltk.tokenize
import re
from collections import Counter
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class RecommendingEngine:

    @staticmethod
    def simple_word_count(job_description, resume):
        job_desc_token = nltk.tokenize.word_tokenize(job_description)
        # resume_token = nltk.tokenize.word_tokenize(resume)

        sorted_job_token = sorted(job_desc_token, key=len, reverse=True)
        pattern = re.compile(
            '(?:\b{}\b)'.format('|'.join(map(re.escape, sorted_job_token)))
        )

        matches = pattern.findall(resume)
        word_count = Counter(matches)
        resume_score = 0
        for word, freq in word_count.items():  # limits to 5 per term
            if freq > 5:
                word_count[word] = 5
                resume_score += 5

            resume_score += freq

        max_score = len(job_desc_token) * 5 # max possible score is all words in job desc 5 times each
        score_norm = resume_score/max_score

        if score_norm > 1:
            return 1
        else:
            return score_norm
        
    @staticmethod
    def levenshtein_ratio(job_description, resume):
        ratio = Levenshtein.ratio(job_description, resume)
        return ratio

    @staticmethod
    def calculate_cosine_similarity(job_description, resume):
        unvector = [job_description, resume]
        vectorizer = CountVectorizer().fit_transform(unvector)
        vectors = vectorizer.toarray()

        vec0 = vectors[0].reshape(1, -1)
        vec1 = vectors[1].reshape(1, -1)
        similarity = cosine_similarity(vec0, vec1)[0][0]
        return similarity

    def __init__(self):
        print('Starting recommending engine...')
        self.steps = {  # weight, function
            'Simple word count': (0.3, RecommendingEngine.simple_word_count),
            'Levenshtein ratio': (0.3, RecommendingEngine.levenshtein_ratio),
            'Cosine similarity': (0.4, RecommendingEngine.calculate_cosine_similarity)
            # 'Cosine similarity': (0.15, RecommendingEngine.simple_word_count,),
            # 'Generic gensim': (0.1, RecommendingEngine.simple_word_count,),
        }

        nltk.download('punkt', quiet=True)

    def load_job_description(self, job_description):
        self.job_description = job_description

    def load_job_description_pickle(self, pickle_file):
        self.job_description = pickle.load(open(pickle_file, 'rb'))

    def load_resumes(self, resumes):
        self.resumes = resumes

    def load_resumes_pickle(self, pickle_file):
        self.resumes = pickle.load(open(pickle_file, 'rb'))
    
    def run_steps(self):
        scores = {}
        for file_path, resume in self.resumes:
            scores[file_path] = {}
            for name, step in self.steps.items():
                weight = step[0]
                function = step[1]
                scores[file_path][name] = function(self.job_description, resume) * weight
        
        self.scores = scores
        return scores

    def get_scores(self):
        final_scores = {}
        for resume, methods in self.scores.items():
            final_score = 0
            for method_score in methods.values():
                final_score += method_score
            
            final_scores[resume] = final_score

        self.final_scores = final_scores
        return final_scores

    def get_five_best_scores(self):
        ordered_scores = list(sorted(self.final_scores.items(), key=lambda item: item[1]))
        best_five_scores = ordered_scores[::-1][:5]
        best_five_resumes = []
        for resume, score in best_five_scores:
            best_five_resumes.append(resume)
            resume_name = resume.split('/')[-1]
            print(f'{resume_name}: {score}')

        return best_five_resumes


if __name__ == '__main__':
    resumes = 'pickle_dev\processed_resumes.pickle'
    job_description = 'pickle_dev\processed_job_description.pickle'

    recommending_engine = RecommendingEngine()
    recommending_engine.load_job_description_pickle(job_description)
    recommending_engine.load_resumes_pickle(resumes)

    scores = recommending_engine.run_steps()
    final_scores = recommending_engine.get_scores()
    best_five = recommending_engine.get_five_best_scores()
    print(1)