"""Optuna optimization

Requires optuna https://optuna.readthedocs.io/en/stable/index.html
Requires mysql https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/
Requires mysql-connector-python https://pypi.org/project/mysql-connector-python/
Requires psycopg for postgresql https://www.psycopg.org/
Requires plotly for visualization https://plotly.com/
Parallelization https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html
Multi-objective https://optuna.readthedocs.io/en/v2.7.0/tutorial/20_recipes/002_multi_objective.html
Pruners https://optuna.readthedocs.io/en/stable/reference/pruners.html#module-optuna.pruners
Samplers https://optuna.readthedocs.io/en/stable/reference/samplers.html#module-optuna.samplers
Nan https://optuna.readthedocs.io/en/stable/faq.html#how-are-nans-returned-by-trials-handled
States https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState
1. TODO sklearn? https://scikit-learn.org/stable/modules/grid_search.html
2. TODO hyperopt? http://hyperopt.github.io/hyperopt/
3. TODO multiprocessing logging (frozen by now) https://optuna.readthedocs.io/en/latest/faq.html#how-to-suppress-log-messages-of-optuna
4. TODO Mouse integration
"""
from pathlib import Path
import shutil
import uuid
import logging
import os
from itertools import combinations
import copy
import socket
import platform
import time
import numpy as np

import optuna

from runner.action.optimize.optimize import Optimize
from runner.action.feature.feature import Feature
from runner.action.run.subprocess import Subprocess
from runner.action.set.continuous import Continuous
from runner.action.set.categorical import Categorical
from runner.action.set.discrete import Discrete


class Optuna(Optimize):
    """Optuna optimization action

    Args:
        storage (str): dialect+driver://username:password@host:port/database
            see SQLAlchemy https://docs.sqlalchemy.org/en/14/core/engines.html
        study (str): study unique name
        objectives (dict): route to direction ("minimize" nor "maximize")
        n_trials (int): The number of trials. If this argument is set to None,
            there is no limitation on the number of trials. If timeout is also
            set to None, the study continues to create trials until it receives
            a termination signal such as Ctrl+C or SIGTERM.
        copies (list): list of files/directories to copy in trial sub directory
        parameters (list of str): parameters routes
    """

    def __init__(self, storage=None, study=None, work_path=None,
                 copies=None, links=None,
                 do_clean_work=None, do_clean_study=None, do_clean_trial=None,
                 do_create_study=None, do_read_study=None, do_delete_study=None,
                 parameters=None, objectives=None, constraints=None,
                 sampler=None, sampler_kwargs=None,
                 pruner=None, pruner_kwargs=None,
                 do_results=None, do_csv=None, do_excel=None, do_plot=None,
                 do_plot_pareto=None, do_plot_other=None,
                 results_color_key=None,
                 results_color_scale=None,
                 do_results_color_reverse=None,
                 results_hover_keys=None,
                 do_optimize=None, n_trials=1,
                 do_update=None, trial=None, do_sub_call=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Study
        self.storage = storage
        self.study = str(uuid.uuid4()) if study is None else study
        self.work_path = Path(str(uuid.uuid4())).resolve() if work_path is None else Path(work_path).resolve()
        self.study_path = (self.work_path / self.study).resolve()
        self.do_create_study = True if do_create_study is None else do_create_study
        self.do_read_study = True if do_read_study is None else do_read_study
        self.do_delete_study = False if do_delete_study is None else do_delete_study
        self.copies = [] if copies is None else [Path(x) for x in copies]
        self.links = [] if links is None else [Path(x) for x in links]
        self.do_clean_work = False if do_clean_work is None else do_clean_work
        self.do_clean_study = False if do_clean_study is None else do_clean_study
        self.do_clean_trial = False if do_clean_trial is None else do_clean_trial
        # Optimizer
        self.sampler = sampler
        self.sampler_kwargs = {} if sampler_kwargs is None else sampler_kwargs
        self.pruner = pruner
        self.pruner_kwargs = {} if pruner_kwargs is None else pruner_kwargs
        self.parameters = parameters
        self.objectives = {} if objectives is None else objectives
        self.constraints = [] if constraints is None else constraints
        # Results
        self.do_results = True if do_results is None else do_results
        self.do_csv = True if do_csv is None else do_csv
        self.do_excel = False if do_excel is None else do_excel
        self.do_plot = False if do_plot is None else do_plot
        self.do_plot_pareto = True if do_plot_pareto is None else do_plot_pareto
        self.do_plot_other = True if do_plot_other is None else do_plot_other
        self.results_color_key = results_color_key
        self.results_color_scale = 'Viridis' if results_color_scale is None else results_color_scale
        self.do_results_reverse_color = False if do_results_color_reverse is None else do_results_color_reverse
        self.results_hover_keys = [] if results_hover_keys is None else results_hover_keys
        # Optimize
        self.do_optimize = True if do_optimize is None else do_optimize
        self.n_trials = n_trials
        # Update
        self.do_update = False if do_update is None else do_update
        self.trial = trial
        self.do_sub_call = False if do_sub_call is None else do_sub_call
        # Common
        self.variable2template = None  # Variable to template
        self.feature2route = None  # Feature to route

    class Objective:
        def __init__(self, optuna_action=None):
            self.optuna_action = optuna_action

        def __call__(self, trial):
            # Set user attributes
            def get_ip():
                if platform.system() == 'Windows':  # VPN
                    ip = socket.gethostbyname(socket.getfqdn())
                else:  # Linux, Darwin
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.settimeout(0)
                    try:
                        s.connect(('10.255.255.255', 1))
                        ip = s.getsockname()[0]
                    except Exception:
                        ip = '127.0.0.1'
                    finally:
                        s.close()
                return ip

            trial.set_user_attr('number', trial.number)
            trial.set_user_attr('system.host', socket.getfqdn())
            trial.set_user_attr('system.ip', get_ip())
            trial.set_user_attr('datetime.utc_offset', time.localtime().tm_gmtoff)
            trial.set_user_attr('sampler', self.optuna_action.sampler)
            trial.set_user_attr('pruner', self.optuna_action.pruner)
            for k, v in self.optuna_action.sampler_kwargs.items():
                trial.set_user_attr(f'sampler.{k}', v)
            for k, v in self.optuna_action.pruner_kwargs.items():
                trial.set_user_attr(f'pruner.{k}', v)

            # TODO multiprocessing logging
            if self.optuna_action.executor is not None:
                optuna.logging.set_verbosity(optuna.logging.WARNING)

            # Copy data
            trial_path = self.optuna_action.study_path / str(trial.number)
            trial_path = trial_path.resolve()
            trial_path.mkdir(parents=True, exist_ok=True)
            for p in self.optuna_action.copies:
                if p.is_dir():
                    shutil.copytree(p, trial_path / p.name)
                elif p.is_file():
                    shutil.copy(p, trial_path)
                else:
                    raise ValueError(p)
            for link in self.optuna_action.links:
                if link.is_dir():
                    os.symlink(link, trial_path / link.name,
                               target_is_directory=True)
                elif link.is_file():
                    os.symlink(link, trial_path / link.name,
                               target_is_directory=False)
                else:
                    raise ValueError(link)
            root = Path().resolve()
            os.chdir(trial_path)

            # Replace variables
            self.optuna_action.replace_variables(kind='suggested', trial=trial)

            # Run action recursively
            # TODO implement this with callbacks?
            def run(action, trial):
                for a in action.sub_actions:
                    # Stop if failed constraints
                    for c in self.optuna_action.constraints:
                        if not trial.user_attrs.get(c, True):
                            return float('nan')
                    a.pre_call()
                    run(a, trial)
                    a.post_call()
                    # Save Feature values to trial
                    if isinstance(a, Feature):
                        r = self.optuna_action.feature2route[a]
                        v = a.value
                        v = int(v) if isinstance(a.value, np.int32) else v
                        trial.set_user_attr(f'features_{r}', v)
                    # Stop if subprocess failed
                    elif isinstance(a, Subprocess):
                        if a.result is None or a.result.returncode != 0:
                            return float('nan')

            run(self.optuna_action, trial)

            # Reset variables
            self.optuna_action.replace_variables(kind='template')

            # Return values
            values = []
            for i, (k, v) in enumerate(self.optuna_action.objectives.items()):
                value = trial.user_attrs.get(f'features_{k}', None)
                values.append(float('nan') if value is None else value)
                trial.set_user_attr(f'values_{i}_{k}', value)

            # Clean data
            os.chdir(root)
            if self.optuna_action.do_clean_trial:
                shutil.rmtree(trial_path, ignore_errors=True)
            return tuple(values)

    def pre_call(self, *args, **kwargs):
        # TODO multiprocessing logging
        optuna.logging.enable_propagation()  # Propagate logs to the root logger.
        optuna.logging.disable_default_handler()  # Stop showing logs in sys.stderr.
        # Study
        root = Path().resolve()
        self.study_path.mkdir(parents=True, exist_ok=True)
        self.study_path = self.study_path.resolve()
        if self.do_delete_study:
            optuna.delete_study(storage=self.storage, study_name=self.study)
            if self.do_clean_study:
                shutil.rmtree(self.study_path, ignore_errors=True)
            return
        # Create
        study = self.create_study()
        # Optimize
        if self.do_optimize:
            study.optimize(func=self.Objective(self), n_trials=self.n_trials,
                           timeout=self.timeout)  # TODO timeout from executor?
        # Results
        if self.do_results:
            self.write_results(study)
        # Update
        if self.do_update:
            self.update(study)
        # Clean
        os.chdir(root)
        if self.do_clean_study:
            shutil.rmtree(self.study_path, ignore_errors=True)
        if self.do_clean_work:
            shutil.rmtree(self.work_path, ignore_errors=True)

    def sub_call(self, *args, **kwargs):
        if self.do_sub_call:
            super().sub_call(*args, **kwargs)

    def replace_variables(self, kind='suggested', trial=None):
        if self.variable2template is None:
            self.variable2template = {}
            g = self.get_graph()
            for p, cs in g.items():
                if isinstance(p, (Continuous, Discrete, Categorical)):
                    self.variable2template.setdefault(p, copy.copy(p))
                for c in cs:
                    if isinstance(c, (Continuous, Discrete, Categorical)):
                        self.variable2template.setdefault(c, copy.copy(c))
        if self.parameters is None or self.feature2route is None:
            routes = self.get_routes()
            if self.parameters is None:
                self.parameters = [k for k, v in routes.items()
                                   if isinstance(v, Feature)]
            if self.feature2route is None:
                self.feature2route = {v: k for k, v in routes.items()
                                      if isinstance(v, Feature)}
        for v, t in self.variable2template.items():
            f = v.get_action(v.route)  # Feature
            r = self.feature2route[f]  # Route to Feature
            if r not in set(self.parameters):  # Replace parameters only
                continue
            if isinstance(v, Continuous):
                if kind == 'suggested':
                    value = trial.suggest_float(name=r, low=t.low, high=t.high)
                    v.low, v.high = value, value
                elif kind == 'optimized':
                    value = trial.user_attrs[f'features_{r}']
                    v.low, v.high = value, value
                elif kind == 'template':
                    v.low, v.high = t.low, t.high
                else:
                    raise ValueError(kind)
            elif isinstance(v, Discrete):
                if kind == 'suggested':
                    if isinstance(t.low, int) and isinstance(t.high, int):
                        s = (t.high - t.low) // (t.num - 1) if t.num != 1 else 1
                        value = trial.suggest_int(name=r, low=t.low, high=t.high, step=s)
                    else:
                        s = (t.high - t.low) / (t.num - 1) if t.num != 1 else 1
                        value = trial.suggest_float(name=r, low=t.low, high=t.high, step=s)
                    v.low, v.high, v.num = value, value, 1
                elif kind == 'optimized':
                    value = trial.user_attrs[f'features_{r}']
                    v.low, v.high, v.num = value, value, 1
                elif kind == 'template':
                    v.low, v.high, v.num = t.low, t.high, t.num
                else:
                    raise ValueError(kind)
            elif isinstance(v, Categorical):
                if kind == 'suggested':
                    value = trial.suggest_categorical(name=r, choices=t.choices)
                    v.choices = [value]
                elif kind == 'optimized':
                    value = trial.user_attrs[f'features_{r}']
                    v.choices = [value]
                elif kind == 'template':
                    v.choices = t.choices
                else:
                    raise ValueError(kind)
            else:
                raise ValueError('Optuna works with Continuous, Discrete '
                                 'and Categorical variables only!')

    def create_study(self):
        if self.sampler is not None:
            sampler = getattr(optuna.samplers, self.sampler)(**self.sampler_kwargs)
        else:
            sampler = None
        if self.pruner is not None:
            pruner = getattr(optuna.pruners, self.pruner)(**self.pruner_kwargs)
        else:
            pruner = None
        if self.do_create_study:
            if self.do_read_study:
                load_if_exists = True  # Raise exception if exists
            else:
                load_if_exists = False  # Load if exists
            if len(self.objectives) == 1:
                direction = list(self.objectives.values())[0]
                study = optuna.create_study(storage=self.storage,
                                            study_name=self.study,
                                            load_if_exists=load_if_exists,
                                            sampler=sampler,
                                            pruner=pruner,
                                            direction=direction)
            elif len(self.objectives) > 1:  # Multi-objective
                directions = list(self.objectives.values())
                study = optuna.create_study(storage=self.storage,
                                            study_name=self.study,
                                            load_if_exists=load_if_exists,
                                            sampler=sampler,
                                            pruner=pruner,
                                            directions=directions)
            else:
                raise ValueError(f'No objectives: {self.objectives}!')
        else:
            if self.do_read_study:
                study = optuna.load_study(storage=self.storage,
                                          study_name=self.study,
                                          sampler=sampler,
                                          pruner=pruner)
                try:
                    self.objectives = {'value': study.direction.name.lower()}
                except RuntimeError:
                    objectives = {f'values_{i}': x.name.lower()
                                  for i, x in enumerate(study.directions)}
                    df = study.trials_dataframe()
                    for k in list(objectives.keys()):
                        s = f'user_attrs_{k}_'
                        for c in df.columns:
                            if c.startswith(s):
                                objectives[c[len(s):]] = objectives.pop(k)
                    self.objectives = objectives
            else:
                raise ValueError('do_crate_study and/or do_read_study should be set')
        return study

    def update(self, study):
        trial = None
        if self.trial is not None:  # Use trial by index
            if self.trial < len(study.trials):
                trial = study.trials[self.trial]
        else:  # Use best trial
            if study.directions is not None:
                if len(study.best_trials) > 0:
                    trial = study.best_trials[0]
            elif study.direction is not None:
                trial = study.best_trial
        if trial is not None:
            logging.info(f'Updating parameters with trial number {trial.number}.')
            self.replace_variables(kind='optimized', trial=trial)
        else:
            logging.warning(f'No trial in study {self.study} to update parameters! '
                            f'Using default parameters...')

    def write_results(self, study):
        if len(study.trials) == 0:
            logging.warning(f'No trials in study {self.study} to write/plot!')
            return
        p = self.study_path
        if self.do_csv:
            try:  # required pandas
                study.trials_dataframe().to_csv(p / 'data.csv')
            except Exception as e:
                print(e)
        if self.do_excel:
            try:  # required pandas
                study.trials_dataframe().to_excel(p / 'data.xlsx')
            except Exception as e:
                print(e)
        if not self.do_plot:
            return
        # Pareto front
        if self.do_plot_pareto:
            if len(self.objectives) > 1:
                try:  # required plotly
                    import plotly.express as px

                    n = len(self.objectives)
                    ns = list(self.objectives.keys())
                    ds = list(self.objectives.values())
                    df = study.trials_dataframe()
                    old2new = {f'values_{i}': f'values_{x}' for i, x in enumerate(ns)}
                    df = df.rename(columns=old2new)
                    hover_data = []
                    for c in df.columns:
                        if c.startswith('params_'):
                            hover_data.append(c)
                        elif c.startswith('values_'):
                            hover_data.append(c)
                        elif c.startswith('user_attrs_'):
                            if c[len('user_attrs_'):] in self.results_hover_keys:
                                hover_data.append(c)
                            elif c in ['user_attrs_datetime.utc_offset',
                                       'user_attrs_system.host',
                                       'user_attrs_system.ip']:
                                hover_data.append(c)
                        elif c in ['duration', 'datetime_start',
                                   'datetime_complete']:
                            hover_data.append(c)
                    if self.results_color_key is not None:
                        color = f'user_attrs_{self.results_color_key}'
                    else:
                        color = None
                    if self.do_results_reverse_color:
                        self.results_color_scale += '_r'
                    for c in combinations(range(n), 2):
                        c_vs = [old2new[f'values_{x}'] for x in c]
                        c_ns = [ns[x] for x in c]
                        c_ds = [ds[x] for x in c]
                        labels = dict(zip(c_vs, c_ns))
                        fig = px.scatter(
                            df, x=c_vs[0], y=c_vs[1],
                            color=color,
                            color_continuous_scale=self.results_color_scale,
                            hover_name="number",
                            hover_data=hover_data,
                            labels=labels)
                        if color is not None:
                            fig.layout.coloraxis.colorbar.title = color
                        fig.write_html(p / f"pareto_front-{'-'.join(f'{n}-{d}' for n, d in zip(c_ns, c_ds))}.html")
                    for c in combinations(range(n), 3):
                        c_vs = [old2new[f'values_{x}'] for x in c]
                        c_ns = [ns[x] for x in c]
                        c_ds = [ds[x] for x in c]
                        labels = dict(zip(c_vs, c_ns))
                        fig = px.scatter_3d(
                            df, x=c_vs[0], y=c_vs[1], z=c_vs[2],
                            color=color,
                            color_continuous_scale=self.results_color_scale,
                            hover_name="number",
                            hover_data=hover_data,
                            labels=labels)
                        if color is not None:
                            fig.layout.coloraxis.colorbar.title = color
                        fig.write_html(p / f"pareto_front-{'-'.join(f'{n}-{d}' for n, d in zip(c_ns, c_ds))}.html")
                except Exception as e:
                    print(e)
        if self.do_plot_other:
            for i, (n, d) in enumerate(self.objectives.items()):
                try:  # required plotly
                    optuna.visualization.plot_optimization_history(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"optimization_history-{d}-{n}.html")
                    optuna.visualization.plot_slice(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"slice-{d}-{n}.html")
                    optuna.visualization.plot_contour(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"contour-{d}-{n}.html")
                    optuna.visualization.plot_parallel_coordinate(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"parallel_coordinate-{d}-{n}.html")
                    optuna.visualization.plot_edf(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"edf-{d}-{n}.html")
                except Exception as e:
                    print(e)
                try:  # required sklearn
                    optuna.visualization.plot_param_importances(
                        study, target_name=n, target=lambda x: x.values[i]).write_html(
                        p / f"param_importances-{d}-{n}.html")
                except Exception as e:
                    print(e)
