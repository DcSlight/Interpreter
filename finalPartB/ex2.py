from functools import reduce

str_list = ["hello", "welcome", "here"]

x = reduce((lambda x, y: x + ' ' + y), str_list)

print(x)
