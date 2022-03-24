from runner.action.feature.feature import Feature
from runner.action.set.discrete import Discrete


class FeatureDiscrete(Feature):
    """Discrete feature

    Alias for Feature with set.Discrete first sub action

    Args:
        low (float): low boundary
        high (float): high boundary
        num (int): number of steps
        route (str): route to value (see Action)
    """

    def __init__(self, low=0.0, high=1.0, num=None, route='.~~', **kwargs):
        d = Discrete(low=low, high=high, num=num, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, d)
        super().__init__(**kwargs)
