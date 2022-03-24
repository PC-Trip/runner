from pathlib import Path

import yaml

from runner.action.get.file.markup.markup import Markup


class Yaml(Markup):
    """Write YAML to existing or new YAML with template

    Args:
        template (dict): dictionary template
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        output_path (str): path to output file
        remove_input (bool): remove input file if it exists
    """
    def __init__(self, template, pattern='\$[^\s$]*\$', input_path=None,
                 output_path=None, remove_input=False, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.pattern = pattern
        self.input_path = input_path
        self.output_path = input_path if output_path is None else output_path
        if self.output_path is None:
            raise ValueError(f"Output or input file doesn't set!")
        self.remove_input = remove_input

    def post_call(self, *args, **kwargs):
        if self.input_path is not None:
            p = Path(self.input_path)
            with open(p) as f:
                layout = yaml.safe_load(f)
            if self.remove_input:
                p.unlink()
        else:
            layout = {}
        layout = Markup.update(self, layout, self.template, self.pattern)
        p = Path(self.output_path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w') as f:
            yaml.safe_dump(layout, f)
