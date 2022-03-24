"""FOAM dictionary

TODO parse list, table, vector, tensor
"""
from pathlib import Path

from runner.action.get.file.markup.markup import Markup


class Foam(Markup):
    def __init__(self, template, pattern='\$[^\s$]*\$', input_path=None,
                 output_path=None, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        for k in list(self.template.keys()):
            if k == '':
                self.template[None] = self.template.pop(k)
        self.pattern = pattern
        self.input_path = input_path
        self.output_path = input_path if output_path is None else output_path
        if self.output_path is None:
            raise ValueError(f"Output or input file doesn't set!")

    def post_call(self, *args, **kwargs):
        layout = self.load(self.input_path)
        layout = Markup.update(self, layout, self.template, self.pattern)
        self.dump(layout, self.output_path)

    @staticmethod
    def load(path):
        layout = {}
        if path is not None:
            p = Path(path)
            with open(p) as f:
                name, kvs = Foam.load_object(f)
                while name is not None or len(kvs) > 0:
                    layout[name] = kvs
                    name, kvs = Foam.load_object(f)
        return layout

    @staticmethod
    def load_object(f, name=None):
        kvs = {}  # key-values
        is_comment = False
        for line in f:
            line = line.strip()
            if line.startswith('/*'):
                is_comment = True
            if line.endswith('*/'):
                is_comment = False
                continue
            if line.startswith('//') or line == '':
                continue
            if not is_comment:
                line = line.split('//')[0].strip()  # remove inline comments
                line = line.replace(';', '')  # remove ending ;
                ts = line.split()  # tokens
                k, vs = ts[0], ts[1:]
                if len(vs) == 0:
                    if k == '{':
                        continue
                    elif k == '}':
                        break
                    elif name is None and len(kvs) == 0:
                        name = k
                    else:
                        sub_name, sub_kvs = Foam.load_object(f, k)
                        kvs[sub_name] = sub_kvs
                elif len(vs) == 1:
                    kvs[k] = vs[0]
                else:  # list
                    if vs[0] in ('uniform', 'nonuniform', 'constant'):  # Workaround
                        k += f' {vs[0]}'
                        vs = vs[1:]
                    new_vs = []
                    for v in vs:
                        v = v.replace('(', '').replace(')', '')
                        if v != '':
                            new_vs.append(v)
                    kvs[k] = new_vs
        return name, kvs

    @staticmethod
    def dump(dictionary, path):
        p = Path(path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            for name, kvs in dictionary.items():
                Foam.dump_object(name, kvs, f)

    @staticmethod
    def dump_object(name, kvs, f):
        if name is not None:
            f.write(f'{name}\n')
            f.write('{\n')
        for k, v in kvs.items():
            if isinstance(v, list):
                f.write(f'{k} ({" ".join([str(x) for x in v])});\n')
            elif isinstance(v, dict):
                Foam.dump_object(k, v, f)
            else:
                f.write(f'{k} {v};\n')
        if name is not None:
            f.write('}\n')
