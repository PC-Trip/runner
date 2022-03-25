from runner.action.feature.feature import Feature
from runner.action.set.file.regex import Regex


class FeatureRegex(Feature):
    """Regex feature

    Alias for Feature with set.file.Regex first sub action

    Args:
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        value_type (str): type of input value(s)
        read_type (str): "line" - read file by line, "all" - read entire file
        index (int or list): index(es) in list of found values, None - get all values
        line_index (int or list): index(es) in list of found values in line, None - get all values
        line_start (int): line to start from
        route (str): route to value (see Action)
    """

    def __init__(self, pattern, input_path, value_type='str', read_type='line',
                 index=0, line_index=None, line_start=0, route='.~~', **kwargs):
        r = Regex(pattern, input_path, value_type=value_type, read_type=read_type,
                  index=index, line_index=line_index, line_start=line_start,
                  route=route)
        kwargs.setdefault('sub_actions', []).insert(0, r)
        super().__init__(**kwargs)
