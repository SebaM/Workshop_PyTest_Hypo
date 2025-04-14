from numbers import Number


def square(given: float) -> float:
    return given * given


def is_even(num):
    return all(int(d) % 2 == 0 for d in str(abs(num)))


def add(given_1, given_2):
    if type(given_1) is not int:
        raise ValueError("Unsupported type for given value")
    has_three_or_more = lambda num: len(str(num).split('.')[1]) >= 3 if '.' in str(num) else False
    if has_three_or_more(given_2):
        print(has_three_or_more(given_2))
        raise ValueError("For currency I can not have more than 1 cent")
    if is_even(given_1) and is_even(given_2):
        raise ValueError("Both are even, how come?!")
    return given_1 + given_2


def divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Cannot divide by zero")
    else:
        return numerator / denominator


def is_right_for_discount(amount: Number) -> [True, False]:
    if amount < 100:
        return False
    elif amount > 100:
        return True
