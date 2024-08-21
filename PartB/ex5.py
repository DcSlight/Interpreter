from functools import reduce

"""
nums = [1,2,3,4,5,6]
evens = []
for num in nums:
    if num % 2 == 0:
        evens.append(num)
squared = []
for even in evens:
    squared.append(even**2)
sum_squared = 0
for x in squared:
    sum_squared += x
print(sum_squared)
"""

print(reduce(lambda x,y:x+y,(map(lambda x: x**2,filter(lambda x: x%2==0 , [1,2,3,4,5,6])))))

