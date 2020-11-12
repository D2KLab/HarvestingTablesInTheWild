import pytest

from core.parsing.utils import check_body_cell_layout
from core.parsing.exceptions import InvalidTableException

def test_check_body_cell_layout():
    # should not raise an exception
    assert check_body_cell_layout([
        ["A", "B", "C"],
        ["1", "2", "3"],
        ["4", "5", "6"],
    ])

    # should raise an exception (too short)
    with pytest.raises(InvalidTableException):
        check_body_cell_layout([
            ["1", "2", "3"],
        ])

    # should raise an exception (irregular layout)
    with pytest.raises(InvalidTableException):
        check_body_cell_layout([
            ["A", "B", "C"],
            ["1", "2", "3"],
            ["4", "5", "6", "7"],
        ])
