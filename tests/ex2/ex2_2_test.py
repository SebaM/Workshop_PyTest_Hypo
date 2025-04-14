import pytest
from source.ex2_1_calculator import add as ex2_1_add, is_right_for_discount


@pytest.mark.parametrize("num1, num2, result", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 1, 1),
    # (1, 2, 3),  # Test case 1: 1 + 2 = 3
    # (0, 0, 0),  # Test case 2: 0 + 0 = 0
    # (-1, -1, -2),  # Test case 3: -1 + -1 = -2
    # (100, 200, 300),  # Test case 4: Large numbers
    # (-5, 5, 0),  # Test case 5: Negative and positive cancel out
])
def test_add_parametrize(num1, num2, result) -> None:
    assert ex2_1_add(num1, num2) == result

# --------------------------------------------------------------------
# if less than 100 no discount
# @pytest.mark.parametrize("", [
#     (2, 3, False),
# ])
# def test_add_parametrize(num1, num2, discount) -> None:
#     assert is_right_for_discount(ex2_1_add(num1, num2)) == discount

