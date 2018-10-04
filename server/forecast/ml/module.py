# Based on https://github.com/henryre/pytorch-fitmodule

from collections import OrderedDict

import numpy as np
import torch
from torch.nn import CrossEntropyLoss, Module, init

from forecast.ml.utils import get_loader, ProgressBar

DEFAULT_LOSS = CrossEntropyLoss()
DEFAULT_BATCH_SIZE = 32


def accuracy(y_true, y_pred):
    return np.mean(y_true.numpy() == np.argmax(y_pred.numpy(), axis=1))


class ModuleExt(Module):
    HISTORY_TRAIN_LOSS = 0
    HISTORY_TRAIN_ACC = 1
    HISTORY_VAL_LOSS = 2
    HISTORY_VAL_ACC = 3
    HISTORY_TOTAL = 4

    def __init__(self):
        super(ModuleExt, self).__init__()
        self.history = None

    def init_weights(self, mode='he'):
        """ Initialize model weights.

        Arguments:
            mode: str
                Initialization algorithm: 'he', 'xavier', 'normal'.
        """
        init_impl = None
        if mode == 'he':
            init_impl = init.kaiming_normal_
        elif mode == 'xavier':
            init_impl = init.xavier_normal_
        elif mode == 'normal':
            init_impl = init.normal_
        for m in self.modules():
            if hasattr(m, 'weight') and (mode == 'normal' or m.weight.ndimension() > 1):
                # kaiming_normal_ and xavier_normal_ don't work with less than 2 dimensions
                init_impl(m.weight)
            if hasattr(m, 'bias'):
                m.bias.data.fill_(0.0)

    def fit(self,
            x,
            y,
            optimizer,
            batch_size=DEFAULT_BATCH_SIZE,
            epochs=1,
            verbose=1,
            validation_split=0.,
            validation_data=None,
            shuffle=True,
            initial_epoch=0,
            seed=None,
            loss=DEFAULT_LOSS,
            annealing=None):
        """Trains the model.

        Arguments
            x: training data Tensor.
            y: target data Tensor.
            optimizer: training optimizer object.
            batch_size: integer. Number of samples per gradient update.
            epochs: integer, the number of times to iterate over the training data arrays.
            verbose: 0, 1. Verbosity mode.
                0 = silent, 1 = verbose.
            validation_split: float between 0 and 1:
                fraction of the training data to be used as validation data.
                The model will set apart this fraction of the training data,
                will not train on it, and will evaluate the loss and any model metrics
                on this data at the end of each epoch.
            validation_data: (x_val, y_val) tuple on which to evaluate the loss and any model metrics
                at the end of each epoch. The model will not be trained on this data.
            shuffle: boolean, whether to shuffle the training data before each epoch.
            initial_epoch: epoch at which to start training (useful for resuming a previous training run).
            seed: random seed.
            loss: training loss object.
            annealing: learning rate adjustment object.
        """
        if seed and seed >= 0:
            torch.manual_seed(seed)

        # Prepare validation data
        if validation_data:
            x_val, y_val = validation_data
        elif validation_split and 0. < validation_split < 1.:
            split = int(x.size()[0] * (1. - validation_split))
            x, x_val = x[:split], x[split:]
            y, y_val = y[:split], y[split:]
        else:
            x_val, y_val = None, None

        # Build DataLoaders
        train_data = get_loader(x, y, batch_size, shuffle)

        # Create history
        self.history = np.zeros((epochs - initial_epoch, self.HISTORY_TOTAL), dtype=np.float)

        # Run training loop
        self.train()
        for t in range(initial_epoch, epochs):
            if verbose > 0:
                print("Epoch {0} / {1}".format(t + 1, epochs))
                # Setup logger
                pb = ProgressBar(len(train_data))
            log = OrderedDict()
            epoch_loss = 0.0

            if annealing is not None:
                annealing.step()

            # Run batches
            for batch_i, batch_data in enumerate(train_data):
                # Get batch data
                x_batch, y_batch = batch_data
                # Backpropagation
                optimizer.zero_grad()
                y_batch_pred = self(x_batch)
                batch_loss = loss(y_batch_pred, y_batch)
                batch_loss.backward()
                optimizer.step()
                # Update status
                epoch_loss += batch_loss.item()
                log['train_loss'] = float(epoch_loss) / (batch_i + 1)
                if verbose > 0:
                    pb.bar(batch_i, log)

            # Add history
            y_train_pred = self.predict(x, batch_size, True)
            log['train_acc'] = accuracy(y, y_train_pred)
            if x_val is not None and y_val is not None:
                y_val_pred = self.predict(x_val, batch_size, True)
                val_loss = loss(y_val_pred, y_val)
                log['val_loss'] = val_loss.item()
                log['val_acc'] = accuracy(y_val, y_val_pred)
            self._add_history(t, log)
            if verbose > 0:
                pb.close(log)

    def predict(self, x, batch_size=DEFAULT_BATCH_SIZE, full_output=False):
        """Generates output predictions for the input samples.

        Computation is done in batches.

        # Arguments
            x: input data Tensor.
            batch_size: integer.
            full_output: if True it returns full module output as Tensor.

        # Returns
            prediction Tensor.
        """
        # Build DataLoader
        data = get_loader(x, batch_size=batch_size)

        # Batch prediction
        self.eval()
        r, n = 0, x.size()[0]
        y_pred = None
        for batch_data in data:
            # Predict on batch
            x_batch = batch_data[0]
            y_batch_pred = self(x_batch).data
            # Infer prediction shape
            if r == 0:
                y_pred = torch.zeros((n,) + y_batch_pred.size()[1:])
            # Add to prediction tensor
            y_pred[r: min(n, r + batch_size)] = y_batch_pred
            r += batch_size

        if full_output:
            return y_pred
        return torch.argmax(y_pred, dim=1)

    def _add_history(self, epoch, log):
        for i, v in enumerate(log.values()):
            self.history[epoch, i] = v
