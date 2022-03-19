import json
from pathlib import Path
import logging

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
        self.str2obj = {
            'Action': Action,
            'Subprocess': Subprocess,
            'Feature': Feature,
            'Continuous': Continuous,
            'Discrete': Discrete,
            'Categorical': Categorical,
            'Equation': Equation,
            'Value': Value,
            'SetFileRegex': SetFileRegex,
            'GetFileJson': GetFileJson,
            'GetFileFoam': GetFileFoam,
            'GetFileTemplate': GetFileTemplate
        }

        try:
            from action.optimize.optuna import Optuna
            self.str2obj['Optuna'] = Optuna
        except ModuleNotFoundError as e:
            logging.warning(e)
            logging.warning('To use optuna run: pip install -r requirements/optuna.txt '
                            'or pip install -r requirements/optuna_post.txt with post-processing features')

    def __call__(self, obj):
        if isinstance(obj, dict):
            if 'class' in obj:
                key, args, kwargs = obj.pop('class'), [], obj
            else:
                raise FactoryClassError(obj)
        elif isinstance(obj, list) and len(obj) > 1:
            key, args, kwargs = obj[0], obj[1:], {}
        elif isinstance(obj, str):
            p = Path(obj)
            if p.is_file() and p.suffix == '.json':
                with open(p) as f:
                    data = json.load(f)
                if 'class' in obj:
                    key, args, kwargs = data.pop('class'), [], data
                else:
                    raise FactoryClassError(obj)
            else:
                key, args, kwargs = obj, [], {}
        else:
            raise FactoryValueError(obj)
        if isinstance(key, str) and key in self.str2obj:
            return self.str2obj[key](*args, **kwargs)
        else:
            raise FactoryKeyError(key)
