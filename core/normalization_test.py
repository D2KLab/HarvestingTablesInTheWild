from core.normalization import clean_unicode, clean_whitespace, get_n_most_common_terms


def test_get_n_most_common_terms():
    assert get_n_most_common_terms(
        "Hello here, hello there, hello everywhere.", 1) == ["hello"]
    assert get_n_most_common_terms(
        (
            "first first first "
            "second second "
            "third"
        ), 2) == ["first", "second"]


def test_clean_unicode():
    assert clean_unicode(
        "sentence with confusable dot\u2024") == "sentence with confusable dot."


def test_clean_whitespace():
    assert clean_whitespace("\t\tfoo     bar\n\n\t baz  ") == "foo bar baz"
