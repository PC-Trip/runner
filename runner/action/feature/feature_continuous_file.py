from runner.action.feature.feature import Feature
from runner.action.set.continuous import Continuous
from runner.action.get.file.template import Template


class FeatureContinuousFile(Feature):
    """Continuous feature to file

    Alias for Feature with set.Continuous first sub action and get.file.Template last

    Args:
        low (float): low boundary
        high (float): high boundary
        route (str): route to value (see Action)
        template (str): template or path to template file
        pattern (str): regex expression for wildcards
        output_path (str): path to output file
        remove_template (bool): remove template file if it exists
    """

    def __init__(self, low=0.0, high=1.0, route='.~~', template="$.~~$",
                 pattern='\$[^\s$]*\$', output_path=None, remove_template=False,
                 **kwargs):
        c = Continuous(low=low, high=high, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        t = Template(template=template, output_path=output_path, pattern=pattern,
                     remove_template=remove_template)
        kwargs.setdefault('sub_actions', []).append(t)
        super().__init__(**kwargs)
