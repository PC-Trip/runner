from runner.action.feature.feature import Feature
from runner.action.set.discrete import Discrete
from runner.action.get.file.template import Template


class FeatureDiscreteFile(Feature):
    """Discrete feature to file

    Alias for Feature with set.Discrete first sub action and get.file.Template last

    Args:
        low (float): low boundary
        high (float): high boundary
        num (int): number of steps
        route (str): route to value (see Action)
        template (str): template or path to template file
        path (str): path to output file
        pattern (str): regex expression for wildcards
        remove_template (bool): remove template file if it exists
    """

    def __init__(self, low=0.0, high=1.0, num=None, route='.~~',
                 template="$.~~$", pattern='\$[^\s$]*\$', output_path=None,
                 remove_template=False, **kwargs):
        d = Discrete(low=low, high=high, num=num, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, d)
        t = Template(template=template, output_path=output_path, pattern=pattern,
                     remove_template=remove_template)
        kwargs.setdefault('sub_actions', []).append(t)
        super().__init__(**kwargs)
