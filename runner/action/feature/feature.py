from runner.action.action import Action


class Feature(Action):
    """Feature - action with value

    Args:
        value (object): value of the feature
    """

    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
