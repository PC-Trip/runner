import numpy as np

from runner.action.set.variable import Variable


class Discrete(Variable):
    def __init__(self, low=0, high=1, num=None, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high
        self.num = int(self.high - self.low) + 1 if num is None else num
        self.route = route

    def post_call(self, *args, **kwargs):
        v = np.random.choice(np.linspace(
            self.low, self.high, self.num, endpoint=True))
        if isinstance(self.low, int) and isinstance(self.high, int):
            v = int(v)
        self.set(self.route, v)
