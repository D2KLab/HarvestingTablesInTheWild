import pytest

from core.parsing.utils import validate_body_cell_layout, get_term_set
from core.parsing.exceptions import InvalidTableException

def test_check_body_cell_layout():
    # should not raise an exception
    assert validate_body_cell_layout([
        ["A", "B", "C"],
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]) is None

    # should raise an exception (too short)
    with pytest.raises(InvalidTableException):
        validate_body_cell_layout([
            ["1", "2", "3"],
        ])

    # should raise an exception (irregular layout)
    with pytest.raises(InvalidTableException):
        validate_body_cell_layout([
            ["A", "B", "C"],
            ["1", "2", "3"],
            ["4", "5", "6", "7"],
        ])


def test_get_term_set():
    # wrong input data type
    with pytest.raises(TypeError):
        get_term_set(123)

    # regular test
    check = 'Hello World!\r\nFoo bar FOO  BAR bar BAZ'
    want = ['bar', 'foo', 'hello', 'world!', 'baz']
    got = get_term_set(check)
    assert got == want

    # edge case
    check = "  \r\n \t"
    want = []
    got = get_term_set(check)
    assert got == want
