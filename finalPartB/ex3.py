from functools import reduce


def cumulative_sum_of_squares(lists):
    return list(map(lambda sublist:
                    reduce(lambda y, x: y + x,
                           map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, map(lambda x: x, sublist)))), lists))


print(cumulative_sum_of_squares([[1, 9, 10, 4, 3], [2, 7, 6], [3, 5, 8, 12]]))
