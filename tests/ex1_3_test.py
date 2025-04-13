import unittest

from source.ex1_3_calculator import square as ex1_3_square
import pytest

def test_square():
    # print(f'-------- HERE --------')
    assert ex1_3_square(5) == 25

# def test_square_float():
#     assert ex1_3_square(4.) == 16.
#     # assert ex1_2_square(4.) == pytest.approx(15.)
#
# class TestSquare:
#     def test_square(self) -> None:
#         assert ex1_3_square(8) is 64
#
# # Also other frameworks code as unittest or nose
# class TestSquareUT(unittest.TestCase):
#     def test_square(self) -> None:
#         self.assertGreater(ex1_3_square(3), 9)