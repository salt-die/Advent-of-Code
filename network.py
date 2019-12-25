from computer import Computer

class NetworkedComputer(Computer):
    def __init__(self, *args, feed, **kwargs):
        super().__init__(*args, **kwargs)
        self.iterator = self.compute_iter(feed=feed)
        self.idle = False
        self.produced = True

    def __next__(self):
        for _, op, *_ in self.iterator:
            if op == '03' and not self.feed:
                self << -1
                if not self.produced:
                    self.idle = True
                    return
                else:
                    self.produced = False

            if len(self.out) == 3:
                self.produced = True
                return self.pop(), self.pop(), self.pop()

    def connect(self, *args, **kwargs):
        self.idle = False
        return super().connect(*args, **kwargs)


class NAT:
    def __init__(self, network):
        self.running = True
        self.network = network
        self.xy = self.first = self.last = None

    def wake(self):
        _, y = self.xy
        if self.first is None:
            self.first = y
        if self.last == y:
            self.running = False
        self.last = y
        self.network[0] << self.xy

    def route(self):
        while self.running:
            packets = [packet for computer in self.network
                       if not computer.idle and (packet := next(computer))]
            if not packets:
                self.wake()
                continue
            for address, *xy in packets:
                if address == 255:
                    self.xy = xy
                else:
                    self.network[address] << xy
