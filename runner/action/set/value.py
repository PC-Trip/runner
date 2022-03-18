from runner.action.set.set import Set


class Value(Set):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def post_call(self, *args, **kwargs):
        self.sup_action.value = self.value
