from runner.action.feature.feature import Feature
from runner.action.set.discrete import Discrete
from runner.action.get.file.markup.yaml import Yaml


class FeatureDiscreteYaml(Feature):
    """Continuous feature to YAML file

    Alias for Feature with set.Discrete first sub action and get.file.markup.Json last

    Args:
        low (float): low boundary
        high (float): high boundary
        num (int): number of steps
        route (str): route to value (see Action)
        template (dict): dictionary template
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        output_path (str): path to output file
        remove_input (bool): remove input file if it exists
    """

    def __init__(self, low=0.0, high=1.0, num=None, route='.~~', template=None,
                 pattern='\$[^\s$]*\$', input_path=None, output_path=None,
                 remove_input=False, **kwargs):
        d = Discrete(low=low, high=high, num=num, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, d)
        template = {"value": "$.~~$"} if template is None else template
        y = Yaml(template=template, pattern=pattern, input_path=input_path,
                 output_path=output_path, remove_input=remove_input)
        kwargs.setdefault('sub_actions', []).append(y)
        super().__init__(**kwargs)
