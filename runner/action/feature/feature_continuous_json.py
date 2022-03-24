from runner.action.feature.feature import Feature
from runner.action.set.continuous import Continuous
from runner.action.get.file.markup.json import Json


class FeatureContinuousJson(Feature):
    """Continuous feature to JSON file

    Alias for Feature with set.Continuous first sub action and get.file.markup.Json last

    Args:
        low (float): low boundary
        high (float): high boundary
        route (str): route to value (see Action)
        template (dict): dictionary template
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        output_path (str): path to output file
        remove_input (bool): remove input file if it exists
    """

    def __init__(self, low=0.0, high=1.0, route='.~~', template=None,
                 pattern='\$[^\s$]*\$', input_path=None, output_path=None,
                 remove_input=False, **kwargs):
        c = Continuous(low=low, high=high, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        template = {"value": "$.~~$"} if template is None else template
        j = Json(template=template, pattern=pattern, input_path=input_path,
                 output_path=output_path, remove_input=remove_input)
        kwargs.setdefault('sub_actions', []).append(j)
        super().__init__(**kwargs)
