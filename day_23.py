from network import NetworkedComputer, NAT

with open('input23', 'r') as data:
    data = list(map(int, data.read().split(',')))

router = NAT([NetworkedComputer(int_code=data, feed=i) for i in range(50)])
router.route()
print(router.first_y, router.last_y) #Part 1, Part 2