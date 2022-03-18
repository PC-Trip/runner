"""Get value from Feature to text file by regex pattern

https://docs.python.org/3/library/re.html#re.search

Using last captured group for replacement
"""
import re
from pathlib import Path

from runner.action.get.get import Get


class RegexFile(Get):
    def __init__(self, regex, path, read_type='line', **kwargs):
        super().__init__(**kwargs)
        self.regex = regex
        self.path = path
        self.read_type = read_type

    def post_call(self, *args, **kwargs):
        p = Path(self.path).resolve()
        v = self.sup_action.value
        v = '' if v is None else v
        r = re.compile(self.regex)
        f = open(p)
        if self.read_type == 'line':
            lines = []
            for line in f:
                m = r.search(line)
                if m is not None:
                    repl = ''.join(f'\g<{x + 1}>' for x in range(len(m.groups()) - 1))
                    repl += str(v)
                    line = r.sub(repl=repl, string=line)
                lines.append(line)
            f.close()
            with open(p, "w") as f:
                f.writelines(lines)
        elif self.read_type == 'all':
            text = f.read()
            m = r.search(text)
            if m is None:
                raise ValueError(self.regex)
            repl = ''.join(f'\g<{x + 1}>' for x in range(len(m.groups()) - 1))
            repl += str(v)
            text = r.sub(repl=repl, string=text)
            f.close()
            with open(p, "w") as f:
                f.write(text)
        else:
            raise ValueError(self.read_type)
