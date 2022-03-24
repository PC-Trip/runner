from runner.action.feature.feature import Feature
from runner.action.set.categorical import Categorical


class FeatureCategorical(Feature):
    """Categorical feature

    Alias for Feature with set.Categorical first sub action

    Args:
        choices (list): list of choices
        route (str): route to value (see Action)
    """

    def __init__(self, choices, route='.~~', **kwargs):
        c = Categorical(choices=choices, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        super().__init__(**kwargs)
