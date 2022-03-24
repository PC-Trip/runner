import re
from pathlib import Path

from runner.action.get.file.file import File


class Template(File):
    """Write to file with template

    Args:
        template (str): template or path to template file
        pattern (str): regex expression for wildcards
        output_path (str): path to output file
        remove_template (bool): remove template file if it exists
    """
    def __init__(self, template, pattern='\$[^\s$]*\$',
                 output_path=None, remove_template=False, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.pattern = pattern
        self.output_path = template if output_path is None else output_path
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
        p = Path(self.output_path)
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
