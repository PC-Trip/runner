import numpy as np

from runner.action.set.variable import Variable


class Categorical(Variable):
    def __init__(self, choices, route='.::', **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.route = route

    def post_call(self, *args, **kwargs):
        self.get_routes()[self.route].value = np.random.choice(self.choices)
