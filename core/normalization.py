from typing import List
from collections import Counter

from spacy import load as load_nlp
from confusables import normalize as normalize_unicode

en_nlp = load_nlp('en')


def get_n_most_common_terms(text: str, n: int) -> List[str]:
    doc = en_nlp(text)
    nouns = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    normalized_fields = nouns + verbs

    counter = Counter(normalized_fields)
    most_common_tuples = counter.most_common(n)
    most_common_words = map(lambda tuple: tuple[0], most_common_tuples)
    return list(most_common_words)


def clean_whitespace(text: str) -> str:
    # remove tabs, newlines and other whitespace (also leading/trailing)
    text = ' '.join(text.split())
    return text


def clean_unicode(text: str) -> str:
    possible_normalizations = normalize_unicode(text, prioritize_alpha=True)
    # The first item is closest to the original text
    # https://www.unicode.org/Public/security/latest/confusables.txt
    return possible_normalizations[0]
