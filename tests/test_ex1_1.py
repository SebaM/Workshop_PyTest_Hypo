from source.ex1_2_calculator import square as my_square, add as my_add

def test_assert():
    assert True is False


def assert_with_custom_description_test():
    assert True is False, "In this context this require some more explanation"