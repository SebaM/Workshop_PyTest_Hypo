from source.ex2_1_calculator import add as ex2_1_add


def test_add() -> None:
    assert ex2_1_add(2, 3) == 5, "2 + 3 should be 5"
    assert ex2_1_add(-1, 1) == 0
    assert ex2_1_add(0, 1) == 1


# --------------------------------------------------------------------
# @pytest.mark.parametrize("num1, num2, result", [
#     (2, 3, 5),
#     (-1, 1),
#     (...),
# ])
# def test_add_parametrize(num1, num2, result) -> None:
#     assert ex2_1_add(num1, num2) == result
