from runner.action.feature.feature import Feature
from runner.action.set.continuous import Continuous


class FeatureContinuous(Feature):
    """Continuous feature

    Alias for Feature with set.Continuous first sub action

    Args:
        low (float): low boundary
        high (float): high boundary
        route (str): route to value (see Action)
    """

    def __init__(self, low=0.0, high=1.0, route='.~~', **kwargs):
        c = Continuous(low=low, high=high, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        super().__init__(**kwargs)
