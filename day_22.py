from sympy import mod_inverse

with open('input22', 'r') as data:
    data = data.read().splitlines()

def reduce(MOD, NITER, POS):
    difference, initial = 1, 0    
    for line in data:
        command, *_, N = line.split()
        if N == 'stack':
            difference *= -1
            initial += difference
        elif command == 'cut':
                initial += int(N) * difference
        else:
            difference *= mod_inverse(int(N), MOD)      

    initial *= mod_inverse(1 - difference, MOD) # Geometric series
    difference = pow(difference, NITER, MOD)
    return ((POS - initial) * difference + initial) % MOD

print(reduce(MOD=10007, NITER=-1, POS=2019)) # Part 1
print(reduce(MOD=119315717514047, NITER=101741582076661, POS=2020)) # Part 2
