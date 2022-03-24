from runner.action.feature.feature import Feature
from runner.action.set.equation import Equation


class FeatureEquation(Feature):
    """Equation feature

    Alias for Feature with set.Equation first sub action

    Args:
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        value_type (str): type of input value(s)
        read_type (str): "line" - read file by line, "all" - read entire file
        index (int or list): index(es) in list of found values, None - get all values
        route (str): route to value (see Action)
    """

    def __init__(self, equation, pattern='\$[^\s$]*\$', route='.~~', **kwargs):
        e = Equation(equation=equation, pattern=pattern, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, e)
        super().__init__(**kwargs)
