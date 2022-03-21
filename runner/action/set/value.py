from runner.action.set.set import Set


class Value(Set):
    def __init__(self, value, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.route = route

    def post_call(self, *args, **kwargs):
        self.get_routes()[self.route].value = self.value
