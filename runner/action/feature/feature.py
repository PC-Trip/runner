from runner.action.action import Action


class Feature(Action):
    """Feature - key-value object

    Action tag is replaced by key if tag is None.

    Args:
        key (str): name of the feature
        value (object): value of the feature
    """

    def __init__(self, key=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.value = value
        self.tag = key if self.tag is None else self.tag
