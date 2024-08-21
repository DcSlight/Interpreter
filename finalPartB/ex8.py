get_primes_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)

l = [5, 12, 7, 3, 8, 20, 15, 1, 9, 6]
print(get_primes_desc(l))