import pytest

from core.parsing.utils import validate_body_cell_layout
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
