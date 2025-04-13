def square(given: float) -> float:
    return given * given

def add(given_1, given_2):
    return given_1 + given_2

def divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Cannot divide by zero")
    else:
        return numerator / denominator