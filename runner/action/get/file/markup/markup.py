from copy import deepcopy

from runner.action.get.file.file import File
from runner.action.get.file.template import Template


class Markup(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def update(action, layout, template, pattern):
        if isinstance(template, dict):
            if not isinstance(layout, dict):
                raise ValueError(f'Bad {layout}, {template}')
            for k, v in template.items():
                if isinstance(v, dict):
                    layout[k] = Markup.update(action, layout.get(k, {}), v, pattern)
                elif isinstance(v, list):
                    u = layout.get(k, [])
                    if isinstance(u, list):
                        if len(u) != len(v):
                            layout[k] = v
                        for i, x in enumerate(v):
                            if isinstance(x, dict):
                                layout[k][i] = Markup.update(action, layout[k][i], x, pattern)
                            elif isinstance(x, list):
                                layout[k][i] = Markup.update(action, layout[k][i], x, pattern)
                            elif x is not None:
                                layout[k][i] = Markup.substitute(action, x, pattern)
                    else:
                        raise ValueError(f'Bad {u}, {layout}, {template}')
                else:
                    layout[k] = Markup.substitute(action, v, pattern)
        elif isinstance(template, list):
            if not isinstance(layout, list):
                raise ValueError(f'Bad {layout}, {template}')
            if len(template) != len(layout):
                layout = deepcopy(template)
            for i, x in enumerate(template):
                if isinstance(x, dict):
                    layout[i] = Markup.update(action, layout[i], x, pattern)
                elif isinstance(x, list):
                    layout[i] = Markup.update(action, layout[i], x, pattern)
                elif x is not None:
                    layout[i] = Markup.substitute(action, x, pattern)
        return layout

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
