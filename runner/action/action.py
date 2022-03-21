"""Base class for all actions (processes)

0. TODO Track proposal 3148! https://www.python.org/dev/peps/pep-3148/
1. About python concurrency https://docs.python.org/3/library/concurrency.html
2. TODO Shared memory
    2.1 multithreading (but GIL)
    2.2 multiprocessing https://docs.python.org/3/library/multiprocessing.shared_memory.html
    2.3 redis (memcached, relational DB)
    2.4 Ray? Spark? Dask? https://github.com/ray-project/ray https://blog.dominodatalab.com/spark-dask-ray-choosing-the-right-framework
3. TODO multiprocessing logging
    3.1 https://stackoverflow.com/questions/43949259/processpoolexecutor-logging-failed
    3.2 https://stackoverflow.com/questions/49782749/processpoolexecutor-logging-fails-to-log-inside-function-on-windows-but-not-on-u
4. TODO Handle signals (SIGTERM and SIGINT, etc)
5. TODO delays between jobs/calls?
6. TODO concurrent keep order? (by executor.map https://stackoverflow.com/questions/67189283/how-to-keep-the-original-order-of-input-when-using-threadpoolexecutor)
7. TODO implement stack_trace using traceback or trace modules?
8. TODO implement stack_trace using uid only as key in the database? Redis?
"""
import concurrent.futures
import time
import uuid
import logging


class Action:
    """Base class for all actions (processes)

    Args:
        tag (str): label for the action
        sub_actions (list of Action): children of the action
        sup_action (Action): parent of the action
        jobs (int): number of sub_actions calls, None - infinite
        timeout (float): maximum execution time, None - infinite
        delay (float): delay in seconds before sub_actions call
        routine (str): routine of sub_actions call
            e.g. for 3 sub_actions and 2 jobs:
            scatter - 1, 2, 3, 1, 2, 3; broadcast - 1, 1, 2, 2, 3, 3
        executor (str): "ProcessPoolExecutor" - multiprocessing,
            "ThreadPoolExecutor" - multithreading,
            or None - sequential (see python concurrent.futures)
        executor_kwargs (dict): kwargs for the executor
            (see python concurrent.futures)
        workers (int): alias for "max_workers" in executor_kwargs, None -
            min(32, number of processors on the machine + 4) for multithreading
            and number of processors on the machine for multiprocessing
            (On Windows multiprocessing max_workers must be less than
            or equal to 61)

    Returns:
            None
    """

    def __init__(self, tag=None, sub_actions=None, sup_action=None,
                 jobs=1, timeout=None, delay=0.,
                 routine='scatter', executor=None,
                 executor_kwargs=None, workers=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.uid = str(uuid.uuid4())
        self.tag = tag
        self.sub_actions = [] if sub_actions is None else sub_actions
        self.sup_action = sup_action
        for a in self.sub_actions:
            a.sup_action = self
        self.jobs = jobs
        self.timeout = timeout
        self.delay = delay
        self.routine = routine
        self.executor = executor
        self.executor_kwargs = {} if executor_kwargs is None else executor_kwargs
        self.workers = workers
        if workers is not None:
            self.executor_kwargs['max_workers'] = workers

    def sub_call(self, *args, **kwargs):
        if self.executor is None:  # Sequential
            if self.jobs is None and self.timeout is None:
                while True:
                    time.sleep(self.delay)
                    for c in self.sub_actions:
                        c(*args, **kwargs)
            elif self.jobs is None and self.timeout is not None:
                t = time.time()
                time.sleep(self.delay)
                while time.time() - t < self.timeout:
                    for c in self.sub_actions:
                        c(*args, **kwargs)
                    time.sleep(self.delay)
            elif self.jobs is not None and self.timeout is None:
                time.sleep(self.delay)
                if self.routine == 'scatter':
                    for _ in range(self.jobs):
                        for c in self.sub_actions:
                            c(*args, **kwargs)
                else:  # 'broadcast'
                    for c in self.sub_actions:
                        for _ in range(self.jobs):
                            c(*args, **kwargs)
            else:  # jobs is not None and timeout is not None
                t = time.time()
                time.sleep(self.delay)
                if self.routine == 'scatter':
                    for _ in range(self.jobs):
                        for c in self.sub_actions:
                            if time.time() - t >= self.timeout:
                                break
                            c(*args, **kwargs)
                else:  # 'broadcast'
                    for c in self.sub_actions:
                        for _ in range(self.jobs):
                            if time.time() - t >= self.timeout:
                                break
                            c(*args, **kwargs)
        else:  # Concurrent
            d = 0  # actions done
            executor = getattr(concurrent.futures, self.executor)
            with executor(**self.executor_kwargs) as e:
                w = e._max_workers
                if self.jobs is None and self.timeout is None:
                    while True:
                        time.sleep(self.delay)
                        if self.routine == 'scatter':
                            fs = (e.submit(x,
                                           *args, **kwargs)
                                  for _ in range(w) for x in self.sub_actions)
                        else:  # 'broadcast
                            fs = (e.submit(x, *args, **kwargs)
                                  for x in self.sub_actions for _ in range(w))
                        for f in concurrent.futures.as_completed(fs=fs):
                            f.result()
                        d += len(self.sub_actions) * w
                elif self.jobs is None and self.timeout is not None:
                    t = time.time()
                    time.sleep(self.delay)
                    while time.time() - t < self.timeout:
                        if self.routine == 'scatter':
                            fs = (e.submit(x, *args, **kwargs)
                                  for _ in range(w) for x in self.sub_actions)
                        else:  # 'broadcast
                            fs = (e.submit(x, *args, **kwargs)
                                  for x in self.sub_actions for _ in range(w))
                        try:
                            for f in concurrent.futures.as_completed(
                                    fs=fs, timeout=self.timeout - (time.time() - t)):
                                f.result()
                        except concurrent.futures.TimeoutError as te:
                            u = int(str(te).split('(')[0].strip()) - 1  # actions undone
                        else:
                            u = 0
                        d += len(self.sub_actions) * w - u
                        time.sleep(self.delay)
                else:  # jobs is not None
                    time.sleep(self.delay)
                    if self.routine == 'scatter':
                        fs = (e.submit(x, *args, **kwargs)
                              for _ in range(self.jobs) for x in self.sub_actions)
                    else:  # 'broadcast'
                        fs = (e.submit(x, *args, **kwargs)
                              for x in self.sub_actions for _ in range(self.jobs))
                    try:
                        for f in concurrent.futures.as_completed(
                                fs=fs, timeout=self.timeout):
                            f.result()
                    except concurrent.futures.TimeoutError as te:
                        u = int(str(te).split('(')[0].strip()) - 1  # actions undone
                    else:
                        u = 0
                    d += len(self.sub_actions) * self.jobs - u

    def pre_call(self, *args, **kwargs):
        pass

    def post_call(self, *args, **kwargs):
        pass

    def get_routes(self, routes=None, prev_action=None, route='~~', sep='.', def_tag=''):
        """Recursively get routes from the action to other activities

        Routes are concatenated from action tags and separator.

        Args:
            routes (dict): routes from action to other actions
            prev_action (Action): previous visited action or None at the start
            route (str): current route
            sep (str): separator between visited actions in the route
            def_tag (str): default tag if action tag is None
                or action is a super action

        Returns:
            dict: routes from action to other actions
        """
        routes = {} if routes is None else routes
        if prev_action is None:  # This action is the root node
            if route in routes:
                logging.warning(f'Routing "{route}" conflict! Set tags to actions'
                                f'to resolve it: {routes[route]} {self}')
            routes[route] = self
            if self.sup_action is not None:
                routes = self.sup_action.get_routes(routes, self, route, sep, def_tag)
            for s in self.sub_actions:
                routes = s.get_routes(routes, self, route, sep, def_tag)
        elif prev_action.sup_action == self:  # This action is the super action of previous
            route = sep.join([def_tag, route])
            if route in routes:
                logging.warning(f'Routing "{route}" conflict! Set tags to actions'
                                f'to resolve it: {routes[route]} {self}')
            routes[route] = self
            if self.sup_action is not None:
                routes = self.sup_action.get_routes(routes, self, route, sep, def_tag)
            for s in self.sub_actions:
                if s != prev_action:
                    routes = s.get_routes(routes, self, route, sep, def_tag)
        else:  # This action is a sub action of previous
            route = sep.join([route, def_tag if self.tag is None else self.tag])
            if route in routes:
                logging.warning(f'Routing "{route}" conflict! Set tags to actions'
                                f'to resolve it: {routes[route]} {self}')
            routes[route] = self
            for s in self.sub_actions:
                routes = s.get_routes(routes, self, route, sep, def_tag)
        return routes

    def get_graph(self, graph=None, prev_action=None):
        """Recursively creating parent-children dictionary

        Args:
            graph (dict): parent-children dictionary
            prev_action (Action): previous visited action or None at the start

        Returns:
            dict: parent-children dictionary
        """
        graph = {} if graph is None else graph
        if prev_action is None:  # This action is the root node
            for s in self.sub_actions:
                graph.setdefault(self, []).append(s)
                graph = s.get_graph(graph, self)
        elif prev_action.sup_action == self:  # This action is the super action of previous
            if self.sup_action is not None:
                graph = self.sup_action.get_graph(graph, self)
            for s in self.sub_actions:
                if s != prev_action:
                    graph.setdefault(self, []).append(s)
                    graph = s.get_graph(graph, self)
        else:  # This action is a sub action of previous
            for s in self.sub_actions:
                graph.setdefault(self, []).append(s)
                graph = s.get_graph(graph, self)
        return graph

    def __call__(self, *args, **kwargs):
        stack_trace = [self]
        while stack_trace[-1].sup_action is not None:
            stack_trace.append(stack_trace[-1].sup_action)
        logging.debug(f'{".".join("" if x.tag is None else x.tag for x in stack_trace)}')
        self.pre_call(*args, **kwargs)
        self.sub_call(*args, **kwargs)
        self.post_call(*args, **kwargs)
