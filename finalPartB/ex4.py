'''
Write a higher-order function that takes a binary operation (as a lambda function)
and returns a new function that applies this operation cumulatively to a sequence.
Use this to implement both factorial and exponentiation functions.
'''


def cumulative_operation(operation):
    def apply_operation(seq):
        result = seq[0]
        for element in seq[1:]:
            result = operation(result, element)
        return result

    return apply_operation


def factorial(n):
    return cumulative_operation(lambda x, y: x * y)(range(1, n + 1))


def exponential(base, exp):
    return cumulative_operation(lambda x, y: x * y)([base] * exp)


print(factorial(5))
print(exponential(2, 3))
