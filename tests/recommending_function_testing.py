# %% [markdown]
# #### Recommending functions testing

# %%
import ingesting_engine
import processing_engine

# %%
resume_folder = '/resumes&job_desc_simple/'
job_desc_file = '/resumes&job_desc_simple/oaktree.txt'

# %%
i = ingesting_engine.IngestingEngine()
raw_resume = i.process_folder(resume_folder)
raw_job_desc = i.load_job_description(job_desc_file)

# %%
p = processing_engine.ProcessingEngine('en')
p.load_resumes(raw_resume)
p.load_job_description(raw_job_desc)
job_desc = p.process_job_description()
resumes = p.process_resumes()

# %%
print(resumes[0])

# %% [markdown]
# ---

# %%
import nltk
import nltk.tokenize
import re
from collections import Counter

# %%
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
        # print(word, freq)
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

# %%
job = job_desc
resume_path = resumes[0][0]
resume = resumes[0][1]

# %%
print(simple_word_count(job, resume))

# %% [markdown]
# ---

# %%
import Levenshtein

# %%
def levenshtein_ratio(job_description, resume):
    ratio = Levenshtein.ratio(job_description, resume)
    return ratio

print(levenshtein_ratio(job, resume))

# %% [markdown]
# ---

# %%
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# %%
def calculate_cosine_similarity(job_description, resume):
    unvector = [job_description, resume]
    vectorizer = CountVectorizer().fit_transform(unvector)
    vectors = vectorizer.toarray()

    vec0 = vectors[0].reshape(1, -1)
    vec1 = vectors[1].reshape(1, -1)
    similarity = cosine_similarity(vec0, vec1)[0][0]
    return similarity

# %%
print(calculate_cosine_similarity(job, resume))

# %% [markdown]
# ---

# %%
steps = [
    (0.3, simple_word_count),
    (0.3, levenshtein_ratio),
    (0.4, calculate_cosine_similarity)
]
scores = {}
for path, resume in resumes:
    total_score = 0
    for w, step in steps:
        score = step(job, resume) * w
        # print(score)
        total_score += score
        print('Total score:', total_score)
    scores[path] = total_score

# %%
dict(sorted(scores.items(), key=lambda item: item[1]))

# %%
ordered_scores = list(sorted(scores.items(), key=lambda item: item[1]))
print(ordered_scores)

# %%
def get_five_best_scores(scores):
    ordered_scores = list(sorted(scores.items(), key=lambda item: item[1]))
    best_five_scores = ordered_scores[::-1][:5]
    best_five_resumes = []
    for resume, score in best_five_scores:
        best_five_resumes.append(resume)
        resume_name = resume.split('/')[-1]
        print(f'{resume_name}: {score}')

    return best_five_resumes

print(get_five_best_scores(scores))
