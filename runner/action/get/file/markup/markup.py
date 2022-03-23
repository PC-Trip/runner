from copy import deepcopy

from runner.action.get.file.file import File
from runner.action.get.file.template import Template


class Markup(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def update(d, mapping, action, pattern):
        if isinstance(mapping, dict):
            if not isinstance(d, dict):
                raise ValueError(f'Bad mapping {d}, {mapping}')
            for k, v in mapping.items():
                if isinstance(v, dict):
                    d[k] = Markup.update(d.get(k, {}), v, action, pattern)
                elif isinstance(v, list):
                    u = d.get(k, [])
                    if isinstance(u, list):
                        if len(u) != len(v):
                            d[k] = v
                        for i, x in enumerate(v):
                            if isinstance(x, dict):
                                d[k][i] = Markup.update(d[k][i], x, action, pattern)
                            elif isinstance(x, list):
                                d[k][i] = Markup.update(d[k][i], x, action, pattern)
                            elif x is not None:
                                d[k][i] = Markup.substitute(action, x, pattern)
                    else:
                        raise ValueError(f'Bad mapping {u}, {d}, {mapping}')
                else:
                    d[k] = Markup.substitute(action, v, pattern)
        elif isinstance(mapping, list):
            if not isinstance(d, list):
                raise ValueError(f'Bad mapping {d}, {mapping}')
            if len(mapping) != len(d):
                d = deepcopy(mapping)
            for i, x in enumerate(mapping):
                if isinstance(x, dict):
                    d[i] = Markup.update(d[i], x, action, pattern)
                elif isinstance(x, list):
                    d[i] = Markup.update(d[i], x, action, pattern)
                elif x is not None:
                    d[i] = Markup.substitute(action, x, pattern)
        return d

    @staticmethod
    def substitute(action, template, pattern='\$[^\s$]*\$'):
        if not isinstance(template, str):
            return template
        t = Template.substitute(action, template, pattern)
        if t == 'True':
            t = True
        elif t == 'False':
            t = False
        else:
            try:
                t = int(t)
            except ValueError:
                try:
                    t = float(t)
                except ValueError:
                    pass
        return t
