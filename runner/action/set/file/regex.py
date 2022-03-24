"""Set from file by regex expression

1. Regex groups and ranges https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Groups_and_Ranges
"""

import re
from pathlib import Path
import logging

from runner.action.set.file.file import File


class Regex(File):
    """Set from file with regex pattern

    Args:
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        value_type (str): type of input value(s)
        read_type (str): "line" -read file by line, "all" - entire file
        index (int or list): index(es) in list of found values, None - get all values
        route (str): route to value (see Action)
    """
    def __init__(self, pattern, input_path, value_type='str', read_type='line',
                 index=0, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.input_path = input_path
        self.value_type = value_type
        self.read_type = read_type
        self.index = index
        self.route = route

    str_to_type = {'str': str, 'int': int, 'float': float, 'bool': bool}

    def post_call(self, *args, **kwargs):
        p = Path(self.input_path)
        t = self.str_to_type[self.value_type]  # type
        rs = []  # results
        with open(p) as f:
            if self.read_type == 'line':
                for line in f:
                    r = re.findall(self.pattern, line)
                    rs.extend(r)
            elif self.read_type == 'all':
                rs = re.findall(self.pattern, f.read())
            else:
                raise ValueError(self.read_type)
        if len(rs) == 0:
            v = None
            logging.warning(f'No objects found with pattern {self.pattern}')
        elif isinstance(self.index, list):
            v = [t(rs[x].strip()) for x in self.index]
        elif isinstance(self.index, int):
            v = t(rs[self.index].strip())
        elif self.index is None:
            v = [t(x.strip()) for x in rs]
        else:
            raise ValueError(self.index)
        self.set(self.route, v)
