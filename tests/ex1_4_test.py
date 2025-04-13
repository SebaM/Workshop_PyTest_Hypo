import pytest
from source.ex1_4_calculator import divide as ex1_4_divide, add as ex1_4_add


def test_divide() -> None:
    with pytest.raises(ZeroDivisionError, match=r'must be \d+$'):
        ex1_4_divide(15, 0)

# def test_add() -> None:
#     assert ex1_4_add(2, 3) == 5, "2 + 3 should be 5"
#     assert ex1_4_add(-1, 1) == 0
#     assert ex1_4_add(0,0) == 0