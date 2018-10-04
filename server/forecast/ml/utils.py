# Based on https://github.com/henryre/pytorch-fitmodule

import sys

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset


################################
# Data utils
################################
def get_loader(x, y=None, batch_size=1, shuffle=False):
    """Convert x and y Tensors to a DataLoader

        If y is None, use a dummy Tensor
    """
    if y is None:
        y = torch.Tensor(x.size()[0])
    return DataLoader(TensorDataset(x, y), batch_size, shuffle)


################################
# Logging
################################
class ProgressBar(object):
    def __init__(self, n, length=40, precision=4):
        # Protect against division by zero
        self._n = max(1, n)
        self._nf = float(n)
        self._length = length
        self._precision = precision
        # Pre-calculate the i values that should trigger a write operation
        self._ticks = set([round(i / 100.0 * n) for i in range(101)])
        self._ticks.add(n - 1)
        self.bar(0)

    def bar(self, i, log=None):
        msg = self._log2message(log) if log is not None else ''
        """Assumes i ranges through [0, n-1]"""
        if i in self._ticks:
            b = int(np.ceil(((i + 1) / self._nf) * self._length))
            sys.stdout.write(
                '\r[{0}{1}] {2}%\t{3}'.format('=' * b, ' ' * (self._length - b), int(100 * ((i + 1) / self._nf)), msg))
            sys.stdout.flush()

    def close(self, log):
        msg = self._log2message(log)
        # Move the bar to 100% before closing
        self.bar(self._n - 1)
        sys.stdout.write('{0}\n\n'.format(msg))
        sys.stdout.flush()

    def _log2message(self, log):
        fmt = '{0}: {1:.' + str(self._precision) + 'f}'
        return '    '.join(fmt.format(k, v) for k, v in log.items())
