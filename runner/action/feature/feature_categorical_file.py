from runner.action.feature.feature import Feature
from runner.action.set.categorical import Categorical
from runner.action.get.file.template import Template


class FeatureCategoricalFile(Feature):
    """Categorical feature to file

    Alias for Feature with set.Categorical first sub action and get.file.Template last

    Args:
        choices (list): list of choices
        route (str): route to value (see Action)
        template (str): template or path to template file
        path (str): path to output file
        pattern (str): regex expression for wildcards
        remove_template (bool): remove template file if it exists
    """

    def __init__(self, choices, route='.~~', template="$.~~$",
                 pattern='\$[^\s$]*\$', output_path=None, remove_template=False,
                 **kwargs):
        c = Categorical(choices=choices, route=route)
        kwargs.setdefault('sub_actions', []).insert(0, c)
        t = Template(template=template, output_path=output_path, pattern=pattern,
                     remove_template=remove_template)
        kwargs.setdefault('sub_actions', []).append(t)
        super().__init__(**kwargs)
