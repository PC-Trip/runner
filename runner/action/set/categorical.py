import numpy as np

from runner.action.set.variable import Variable


class Categorical(Variable):
    """Categorical variable

        Random variable from choices

        Args:
            choices (list): list of choices
            route (str): route to value (see Action)

    """
    def __init__(self, choices, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.route = route

    def post_call(self, *args, **kwargs):
        self.set(self.route, np.random.choice(self.choices))
