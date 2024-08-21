def fibonacci(n):
    a, b = 0, 1
    yield a
    yield b
    for _ in range(2, n):
        a, b = b, (lambda x, y: x + y)(a, b)
        yield b


print(list(fibonacci(10)))
