from computer import Computer

with open('input09', 'r') as data:
    data = list(map(int, data.read().split(',')))

tape = Computer(int_code=data)
print(*tape.compute_n(niter=2, feed=(1, 2)))
