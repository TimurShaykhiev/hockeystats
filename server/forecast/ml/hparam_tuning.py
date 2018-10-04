# Based on sklearn
import time

from sklearn.model_selection import ParameterGrid, ParameterSampler, StratifiedKFold
from sklearn.metrics import accuracy_score


class _BaseSearchCV:
    """Base class for hyper parameter search with cross-validation."""

    def __init__(self, model, scoring=None, cv=None, verbose=0):
        self._scoring = scoring if callable(scoring) else accuracy_score
        self._model = model
        self._cv_fold_num = cv
        self._verbose = verbose
        self.best_model = None
        self.best_params = None
        self.best_score = 0.0
        self.results = []

    def fit(self, x, y):
        """Run fit with all sets of parameters.

        Parameters
        ----------
        x : array-like, shape = [n_samples, n_features]
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape = [n_samples] or [n_samples, n_output]
            Target relative to X for classification or regression.
        """
        cv = StratifiedKFold(n_splits=self._cv_fold_num)

        # Regenerate parameter iterable for each fit
        candidate_params = list(self._get_param_iterator())
        n_candidates = len(candidate_params)
        if self._verbose > 0:
            print('\nFitting for each of {0} candidates'.format(n_candidates))

        batch_gen = cv.split(x, y)
        for parameters in candidate_params:
            try:
                train_idx, val_idx = next(batch_gen)
            except StopIteration:
                batch_gen = cv.split(x, y)
                train_idx, val_idx = next(batch_gen)

            net, score, fit_time = self._fit_and_score(x, y, train_idx, val_idx, parameters)

            self.results.append((parameters, score, fit_time))
            if score > self.best_score:
                self.best_score = score
                self.best_params = parameters
                self.best_model = net

    def _fit_and_score(self, x, y, train_idx, val_idx, parameters):
        if self._verbose > 0:
            print('\n============')

        model_params = {k[4:]: v for k, v in parameters.items() if k.startswith('mod_')}
        fit_params = {k[4:]: v for k, v in parameters.items() if k.startswith('fit_')}
        opt_params = {k[4:]: v for k, v in parameters.items() if k.startswith('opt_')}
        ann_params = {k[4:]: v for k, v in parameters.items() if k.startswith('ann_')}

        # Prepare data
        x_train, y_train = x[train_idx], y[train_idx]
        x_val, y_val = x[val_idx], y[val_idx]

        score = 0.0
        start_time = time.time()

        # Create neural net model
        init_weights = model_params.get('init_weights', None)
        if init_weights is not None:
            del(model_params['init_weights'])
        net = self._model(**model_params)
        if init_weights is not None and len(init_weights) > 0:
            net.init_weights(mode=init_weights)

        # Prepare optimizer
        opt_class = opt_params['cls']
        del(opt_params['cls'])
        optimizer = opt_class(net.parameters(), **opt_params)

        # Prepare annealing
        annealing = None
        if len(ann_params) > 0:
            ann_class = ann_params['cls']
            del(ann_params['cls'])
            annealing = ann_class(optimizer, **ann_params)

        try:
            net.fit(
                x_train,
                y_train,
                optimizer,
                validation_data=(x_val, y_val),
                verbose=self._verbose > 1,
                annealing=annealing,
                **fit_params
            )
        except Exception as e:
            fit_time = time.time() - start_time
            print('Error during fit: {}'.format(e))

        else:
            fit_time = time.time() - start_time
            y_pred = net.predict(x_val)
            score = self._scoring(y_val, y_pred)

        if self._verbose > 0:
            print('Parameters: {}'.format(parameters))
            print('Result: score: {}, time: {}'.format(score, fit_time))

        return net, score, fit_time

    def _get_param_iterator(self):
        raise NotImplementedError


class GridSearchCV(_BaseSearchCV):
    """Exhaustive search over specified parameter values for an model.

    Parameters
    ----------
    model : PyTorch module class
        Neural net class to test.

    params : dict
        Dictionary with parameters names (string) as keys lists of parameters to try.
        Model parameter names must start with 'mod_'. To initialize model weights set 'mod_init_weights' to
        '' (no init) or mode name (e.g. 'he' or 'normal').
        Fit parameter names must start with 'fit_'.
        Optimizer parameter names must start with 'opt_'. Class name must be in 'opt_cls'.
        Annealing parameter names must start with 'ann_'. Class name must be in 'ann_cls'.

    scoring : callable
        A callable to evaluate the predictions on the test set.
        If None, the default scorer is used.

    cv : int, optional
        Specify the number of folds in a `(Stratified)KFold`

    verbose : integer
        Controls the verbosity: the higher, the more messages.
    """

    def __init__(self, model, params, scoring=None, cv=3, verbose=0):
        super(GridSearchCV, self).__init__(model=model, scoring=scoring, cv=cv, verbose=verbose)
        self._params = params

    def _get_param_iterator(self):
        return ParameterGrid(self._params)


class RandomSearchCV(_BaseSearchCV):
    """Random search on hyper parameters.

    In contrast to GridSearchCV, not all parameter values are tried out, but
    rather a fixed number of parameter settings is sampled from the specified
    distributions. The number of parameter settings that are tried is given by try_count.

    Parameters
    ----------
    model : PyTorch module class
        Neural net class to test.

    params : dict
        Dictionary with parameters names (string) as keys lists of parameters to try.
        Model parameter names must start with 'mod_'. To initialize model weights set 'mod_init_weights' to
        '' (no init) or mode name (e.g. 'he' or 'normal').
        Fit parameter names must start with 'fit_'.
        Optimizer parameter names must start with 'opt_'. Class name must be in 'opt_cls'.
        Annealing parameter names must start with 'ann_'. Class name must be in 'ann_cls'.

    try_count : int, optional
        Number of parameter settings that are sampled. try_count trades
        off runtime vs quality of the solution.

    scoring : callable, optional
        A callable to evaluate the predictions on the test set.
        If None, the default scorer is used.

    cv : int, optional
        Specify the number of folds in a `(Stratified)KFold`

    verbose : int, optional
        Controls the verbosity: the higher, the more messages.

    random_state : int, RandomState instance or None, optional
        Pseudo random number generator state used for random uniform sampling
        from lists of possible values instead of scipy.stats distributions.
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    """

    def __init__(self, model, params, try_count=10, scoring=None, cv=3, verbose=0, random_state=None):
        self._params = params
        self._try_count = try_count
        self._random_state = random_state
        super(RandomSearchCV, self).__init__(model=model, scoring=scoring, cv=cv, verbose=verbose)

    def _get_param_iterator(self):
        return ParameterSampler(self._params, self._try_count, random_state=self._random_state)
