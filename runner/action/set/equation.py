"""

TODO remove eval?
"""

import re
import numpy as np
import logging

from runner.action.set.variable import Variable
from runner.action.get.file.template import Template


class Equation(Variable):
    def __init__(self, equation, pattern='\$[^\s$]*\$', route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.equation = equation
        self.pattern = pattern
        self.route = route

    def post_call(self, *args, **kwargs):
        r = Template.substitute(self, self.equation, self.pattern)
        v = eval(r)
        if isinstance(v, str):
            if v.isdigit():
                v = int(v)
            else:
                try:
                    v = float(v)
                except ValueError:
                    pass
        self.set(self.route, v)
