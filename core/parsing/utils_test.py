import pytest

from scrapy.selector import Selector

from core.parsing.utils import validate_body_cell_layout, get_term_set, is_in_form
from core.parsing.exceptions import InvalidTableException

# pylint: disable=singleton-comparison
# at least in tests I want to be explicit about comparison


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
    want = ['bar', 'foo', 'hello', 'world', 'baz']
    got = get_term_set(check)
    assert got == want

    # advanced test
    check = 'Foo-bar (1912 - 2000)  /   Lorem _ ipsum.BAR;baz'
    want = ['bar', 'foo', '1912', '2000', 'lorem', 'ipsum', 'baz']
    got = get_term_set(check)
    assert got == want

    # another advanced test
    check = 'To the foo of the bar with a baz in the foo'
    want = ['foo', 'bar', 'baz']
    got = get_term_set(check)
    assert got == want

    # edge case
    check = "  \r\n \t"
    want = []
    got = get_term_set(check)
    assert got == want


def test_is_in_form():
    sel = Selector(text='<html><body><span>good</span></body></html>')
    sel = sel.css('span')
    assert is_in_form(sel) == False

    sel = Selector(
        text='<html><body><form><table>bad</table></form></body></html>')
    sel = sel.css('table')
    assert is_in_form(sel) == True

    sel = Selector(
        text='<html><head><title>Hello</title></head><body><table>World</table></body><html>')
    sel = sel.css('table')
    assert is_in_form(sel) == False
