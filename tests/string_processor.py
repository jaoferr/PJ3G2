import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string as string_module
import re

class StringProcessor:

    def __init__(self, string, lang):
        self.string = string

        self.supported_languages = {
            'en': 'english'
        }
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        self.stopwords = nltk.corpus.stopwords.words(self.supported_languages[lang])
        self.stemmer = SnowballStemmer(self.supported_languages[lang])

    def set_string(self, string):
        self.string = string

    def stem(self):
        token_words = word_tokenize(self.string)
        stem_sentence = []
        for word in token_words:
            s = self.stemmer.stem(word)
            stem_sentence.append(s)
            stem_sentence.append(' ')
        
        self.string = ''.join(stem_sentence)

    def remove_punctuation(self):
        self.string = self.string.translate(str.maketrans('', '', string_module.punctuation))

    def strip(self):
        self.string = self.string.strip()

    def lower(self):
        self.string.lower()

    def process_string(self):
        self.strip()
        self.replace_spaces()
        self.remove_punctuation()
        self.stem()

        return self.string

    def replace_spaces(self):
        pattern = re.compile(r'(/)|(-)')
        self.string = pattern.sub(' ', self.string)

if __name__ == '__main__':
    string = 'having, This/is not-a test of the emergency broadcast system  '
    s = StringProcessor(string, 'en')
    print(s.process_string())
