from runner.action.feature.feature import Feature
from runner.action.set.categorical import Categorical
from runner.action.get.file.markup.yaml import Yaml


class FeatureCategoricalYaml(Feature):
    """Categorical feature to YAML file

    Alias for Feature with set.Categorical first sub action and get.file.markup.Yaml last

    Args:
        choices (list): list of choices
        route (str): route to value (see Action)
        template (dict): dictionary template
        pattern (str): regex expression for wildcards
        input_path (str): path to input file
        output_path (str): path to output file
        remove_input (bool): remove input file if it exists
    """

    def __init__(self, choices, route='.~~', template=None,
                 pattern='\$[^\s$]*\$', input_path=None, output_path=None,
                 remove_input=False, **kwargs):
        c = Categorical(choices=choices, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        template = {"value": "$.~~$"} if template is None else template
        y = Yaml(template=template, pattern=pattern, input_path=input_path,
                 output_path=output_path, remove_input=remove_input)
        kwargs.setdefault('sub_actions', []).append(y)
        super().__init__(**kwargs)
