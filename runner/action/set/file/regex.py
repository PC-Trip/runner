"""Set from file by regex expression

1. Regex groups and ranges https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Groups_and_Ranges
"""

import re
from pathlib import Path
from itertools import chain

from runner.action.set.file.file import File


class Regex(File):
    """Set from file with regex pattern

    Args:
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        value_type (str): type of input value(s)
        read_type (str): "line" -read file by line, "all" - entire file
        index (int or list): index(es) in list of found values, None - get all values
        line_index (int or list): index(es) in list of found values in line, None - get all values
        line_start (int): line to start from
        route (str): route to value (see Action)
    """
    def __init__(self, pattern, input_path, value_type='str', read_type='line', index=0,
                 line_index=None, line_start=0, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.input_path = input_path
        self.value_type = value_type
        self.read_type = read_type
        self.index = index
        self.line_index = line_index
        self.line_start = line_start
        self.route = route

    str_to_type = {'str': str, 'int': int, 'float': float, 'bool': bool}

    def post_call(self, *args, **kwargs):
        p = Path(self.input_path)
        t = self.str_to_type[self.value_type]  # type
        rs = []  # results
        with open(p) as f:
            if self.read_type == 'line':
                for _ in range(self.line_start):
                    next(f)
                if self.line_index is None:
                    for line in f:
                        rs.append(re.findall(self.pattern, line))
                else:
                    for line in f:
                        r = re.findall(self.pattern, line)
                        if len(r) == 0:
                            continue
                        elif isinstance(self.line_index, int):
                            rs.append([r[self.line_index]])
                        elif isinstance(self.line_index, list):
                            rs.append([r[x] for x in self.line_index])
                        else:
                            raise ValueError(self.line_index)
            elif self.read_type == 'all':
                rs = [re.findall(self.pattern, f.read())]
            else:
                raise ValueError(self.read_type)
        c = chain.from_iterable(rs)
        if len(rs) == 0:
            raise ValueError(f'No objects found with pattern {self.pattern}')
        elif isinstance(self.index, int):
            for _ in range(self.index):
                next(c)
            v = t(next(c).strip())
        elif isinstance(self.index, list):
            cnt = 0
            v = []
            for i in self.index:
                for _ in range(i - cnt):
                    next(c)
                v.append(t(next(c).strip()))
                cnt = i + 1
        elif self.index is None:
            v = [t(x.strip()) for x in c]
        else:
            raise ValueError(self.index)
        self.set(self.route, v)
