from pathlib import Path

from runner.load import load
from runner.action.action import Action
from runner.action.run.subprocess import Subprocess
from runner.action.feature.feature import Feature
from runner.action.set.continuous import Continuous
from runner.action.set.discrete import Discrete
from runner.action.set.categorical import Categorical
from runner.action.set.equation import Equation
from runner.action.set.value import Value
from runner.action.set.file.regex import Regex as SetFileRegex
from runner.action.get.file.markup.json import Json as GetFileJson
from runner.action.get.file.markup.foam import Foam as GetFileFoam
from runner.action.get.file.template import Template as GetFileTemplate
from runner.action.optimize.optuna import Optuna
from runner.action.feature.feature_continuous import FeatureContinuous
from runner.action.feature.feature_continuous_file import FeatureContinuousFile
from runner.action.feature.feature_continuous_json import FeatureContinuousJson
from runner.action.feature.feature_continuous_yaml import FeatureContinuousYaml
from runner.action.feature.feature_continuous_foam import FeatureContinuousFoam
from runner.action.feature.feature_discrete import FeatureDiscrete
from runner.action.feature.feature_discrete_file import FeatureDiscreteFile
from runner.action.feature.feature_discrete_json import FeatureDiscreteJson
from runner.action.feature.feature_discrete_yaml import FeatureDiscreteYaml
from runner.action.feature.feature_discrete_foam import FeatureDiscreteFoam
from runner.action.feature.feature_categorical import FeatureCategorical
from runner.action.feature.feature_categorical_file import FeatureCategoricalFile
from runner.action.feature.feature_categorical_json import FeatureCategoricalJson
from runner.action.feature.feature_categorical_yaml import FeatureCategoricalYaml
from runner.action.feature.feature_categorical_foam import FeatureCategoricalFoam
from runner.action.feature.feature_regex import FeatureRegex
from runner.action.feature.feature_equation import FeatureEquation


class FactoryClassError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class FactoryKeyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class FactoryValueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Factory:
    def __init__(self):
        self.string2class = {
            'Action': Action,
            'A': Action,
            'Subprocess': Subprocess,
            'P': Subprocess,
            'Feature': Feature,
            'F': Feature,
            'Continuous': Continuous,
            'SC': Continuous,
            'Discrete': Discrete,
            'SD': Discrete,
            'Categorical': Categorical,
            'ST': Categorical,
            'Equation': Equation,
            'SE': Equation,
            'Value': Value,
            'SV': Value,
            'SetFileRegex': SetFileRegex,
            'SR': SetFileRegex,
            'GetFileJson': GetFileJson,
            'GJ': GetFileJson,
            'GetFileFoam': GetFileFoam,
            'GetFileTemplate': GetFileTemplate,
            'GF': GetFileTemplate,
            'Optuna': Optuna,
            'FeatureContinuous': FeatureContinuous,
            'FC': FeatureContinuous,
            'FeatureContinuousFile': FeatureContinuousFile,
            'FeatureContinuousJson': FeatureContinuousJson,
            'FeatureContinuousYaml': FeatureContinuousYaml,
            'FeatureContinuousFoam': FeatureContinuousFoam,
            'FeatureDiscrete': FeatureDiscrete,
            'FD': FeatureDiscrete,
            'FeatureDiscreteFile': FeatureDiscreteFile,
            'FeatureDiscreteJson': FeatureDiscreteJson,
            'FeatureDiscreteYaml': FeatureDiscreteYaml,
            'FeatureDiscreteFoam': FeatureDiscreteFoam,
            'FeatureCategorical': FeatureCategorical,
            'FT': FeatureCategorical,
            'FeatureCategoricalFile': FeatureCategoricalFile,
            'FeatureCategoricalJson': FeatureCategoricalJson,
            'FeatureCategoricalYaml': FeatureCategoricalYaml,
            'FeatureCategoricalFoam': FeatureCategoricalFoam,
            'FeatureRegex': FeatureRegex,
            'FR': FeatureRegex,
            'FeatureEquation': FeatureEquation,
            'FE': FeatureEquation
        }

    def __call__(self, obj):
        if isinstance(obj, dict):
            if 'class' in obj:
                key, args, kwargs = obj.pop('class'), [], obj
            else:
                raise FactoryClassError(obj)
        elif isinstance(obj, list) and len(obj) > 1:
            key, args, kwargs = obj[0], obj[1:], {}
        elif isinstance(obj, str):
            if obj.startswith('/'):
                p = Path(obj)
                data = load(p)
                if 'class' in data:
                    key, args, kwargs = data.pop('class'), [], data
                else:
                    raise FactoryClassError(obj)
            else:
                key, args, kwargs = obj, [], {}
        else:
            raise FactoryValueError(obj)
        if isinstance(key, str) and key in self.string2class:
            return self.string2class[key](*args, **kwargs)
        else:
            raise FactoryKeyError(key)
