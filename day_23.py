from computer import Computer
from itertools import cycle

with open('input23', 'r') as data:
    data = list(map(int, data.read().split(',')))
    
network = [Computer(int_code=data) for _ in range(50)]
programs = [computer.compute_iter(feed=i) for i, computer in enumerate(network)]

for computer, program in cycle(zip(network, programs)):
    _, op, *_ = next(program)
    if op == '03' and not computer.feed:
        computer << -1
    if len(computer.out) == 3:
        y, x, address = computer.out
        computer.out.clear()
        if address == 255:
            break
        else:
            network[address] << (x, y)

print(y) # Part 1

network = [Computer(int_code=data) for _ in range(50)]
programs = [computer.compute_iter(feed=i) for i, computer in enumerate(network)]

class NAT:
    x = y = None
    last_y = None
    def check_idle():
        if all(not bool(computer.feed) or computer.feed[-1] == -1 for computer in network):
            if NAT.last_y == NAT.y:
                raise StopIteration
            NAT.last_y = NAT.y
            network[0] << (NAT.x, NAT.y)        
    
for computer, program in cycle(zip(network, programs)):
    _, op, *_ = next(program)
    if op == '03' and not computer.feed:
        computer << -1
    if len(computer.out) == 3:
        y, x, address = computer.out
        computer.out.clear()
        if address == 255:
            NAT.x, NAT.y = x, y
            try:
                NAT.check_idle()
            except StopIteration:
                break
        else:
            network[address] << (x, y)
            
print(NAT.y) # Part 2