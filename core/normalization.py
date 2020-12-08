import unicodedata
from typing import List
from collections import Counter

from spacy import load as load_nlp

en_nlp = load_nlp('en')


def get_n_most_common_terms(text: str, n: int) -> List[str]:
    doc = en_nlp(text)
    # Helpful reading:
    # https://spacy.io/usage/linguistic-features
    # https://universaldependencies.org/docs/u/pos/
    pos_blacklist = ['ADP', 'SYM', 'DET', 'PRON', 'PUNCT', 'X']
    normalized_fields = [
        token.lemma_ for token in doc if not token.pos_ in pos_blacklist
    ]

    counter = Counter(normalized_fields)
    most_common_tuples = counter.most_common(n)
    most_common_words = map(lambda tuple: tuple[0], most_common_tuples)
    return list(most_common_words)


def clean_whitespace(text: str) -> str:
    # remove tabs, newlines and other whitespace (also leading/trailing)
    text = ' '.join(text.split())
    return text


def clean_unicode(text: str) -> str:
    # https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization
    return unicodedata.normalize('NFKD', text)
