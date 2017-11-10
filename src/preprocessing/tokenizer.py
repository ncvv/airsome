''' Tokenizer module. '''

import re

from nltk.stem.snowball import SnowballStemmer

class SnowballTokenizer(object):
    ''' Tokenizer which also stems the tokens. '''

    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.token_pattern = re.compile(r"(?u)\b\w\w+\b")

    def __call__(self, doc):
        # Tokenize the input with a regex and stem each token
        return [self.stemmer.stem(t) for t in self.token_pattern.findall(doc)]
