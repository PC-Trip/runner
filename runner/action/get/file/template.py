import re
from pathlib import Path

from runner.action.get.file.file import File


class Template(File):
    def __init__(self, template, path=None, pattern='\$[^\s$]*\$',
                 remove_template=False, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.path = template if path is None else path
        self.pattern = pattern
        self.remove_template = remove_template

    def post_call(self, *args, **kwargs):
        p = Path(self.template)
        if p.is_file():
            with open(p) as f:
                t = f.read()
            if self.remove_template:
                p.unlink()
        else:
            t = self.template
        t = Template.substitute(self, t, self.pattern)
        p = Path(self.path)
        with open(p, 'w') as f:
            f.write(t)

    @staticmethod
    def substitute(action, template, pattern='\$[^\s$]*\$'):
        p = re.compile(pattern)
        m = p.search(template)
        while m is not None:
            route = ''.join([x for x in m.group(0)
                             if x.isalnum() or x in ['.', '~', '_', '-', "'"]])
            value = str(action.get(route))
            template = template[:m.start()] + value + template[m.end():]
            m = p.search(template)
        return template
