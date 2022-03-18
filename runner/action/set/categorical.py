import numpy as np

from runner.action.set.variable import Variable


class Categorical(Variable):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices

    def post_call(self, *args, **kwargs):
        self.sup_action.value = np.random.choice(self.choices)
