input_list = [
    ["level", "world", "deed", "python"],
    ["radar", "hello", "madam", "test", "noon","abba"],
    ["civic", "kayak", "refer"],
    []
]
def ex_6(input_list):
    return [sum(1 for word in l if word == word[::-1]) for l in input_list]

print(ex_6(input_list))