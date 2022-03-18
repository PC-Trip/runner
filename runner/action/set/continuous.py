import numpy as np

from runner.action.set.variable import Variable


class Continuous(Variable):
    def __init__(self, low, high, **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high

    def post_call(self, *args, **kwargs):
        self.sup_action.value = np.random.uniform(self.low, self.high)
