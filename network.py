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
                    return -1, -1, -1
                else:
                    self.produced = False

            if len(self.out) == 3:
                y, x, address = self.out
                self.out.clear()
                self.produced = True
                return address, x, y

    def connect(self, *args, **kwargs):
        Computer.connect(self, *args, **kwargs)
        self.idle = False


class NAT:
    def __init__(self, network):
        self.running = True
        self.network = network
        self.xy = self.first = self.last = None

    def check_idle(self):
        if all(computer.idle for computer in self.network):
            self.wake()

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
            for computer in self.network:
                if computer.idle:
                    continue
                address, *xy = next(computer)
                if address == -1: # Computer has become idle
                    continue
                elif address == 255:
                    self.xy = xy
                else:
                    self.network[address] << xy
            self.check_idle()
