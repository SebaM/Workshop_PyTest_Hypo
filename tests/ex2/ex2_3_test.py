import datetime

import pytest
from hypothesis import settings, Verbosity, given, strategies as st, example

from source.ex2_1_calculator import add as ex2_1_add, is_right_for_discount


@pytest.mark.parametrize("num1, num2, result", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 1, 1),
    (1, 2, 3),  # Test case 1: 1 + 2 = 3
    (0, 0, 0),  # Test case 2: 0 + 0 = 0
    (-1, -1, -2),  # Test case 3: -1 + -1 = -2
    (100, 200, 300),  # Test case 4: Large numbers
    (-5, 5, 0),  # Test case 5: Negative and positive cancel out
])
def test_add_parametrize(num1, num2, result) -> None:
    assert ex2_1_add(num1, num2) == result


# @given(num1=st.decimals(), num2=st.decimals())
# @settings(verbosity=Verbosity.normal, deadline=datetime.timedelta(seconds=30), max_examples=30)
# @example(num1=3, num2=4)
# def test_add_hypothesis_positive(num1, num2) -> None:
#     assert ex2_1_add(num1, num2) == num1 + num2
#

# --------------------------------------------------------------------
# # def my_first_strategy():
# #     return st.one_of(
# #         st.decimals(min_value=0, allow_nan=True, allow_infinity=False, places=3),
# #     )
#
# @given(num1=st.text(), num2=st.text())
# @settings(verbosity=Verbosity.normal, deadline=datetime.timedelta(seconds=30), max_examples=30)
# def test_add_hypothesis_negative(num1, num2) -> None:
#     assert ex2_1_add(num1, num2) == num1 + num2

# --------------------------------------------------------------------
# st.from_regex(r'[a-zA-Z0-9-_:. ()]{50,218}', fullmatch=True)
