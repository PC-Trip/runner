import json
from pathlib import Path

from runner.action.get.file.markup.markup import Markup


class Json(Markup):
    def __init__(self, path, mapping, pattern='\$[^\s$]*\$', output=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.mapping = mapping
        self.pattern = pattern
        self.output = path if output is None else output

    def post_call(self, *args, **kwargs):
        p = Path(self.path)
        with open(p) as f:
            d = json.load(f)
        d = Markup.update(d, self.mapping, self, self.pattern)
        p = Path(self.output)
        with open(p, 'w') as f:
            json.dump(d, f, indent=2)

