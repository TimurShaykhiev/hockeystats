import time
from collections import namedtuple

import numpy as np

INT_ARRAY_DATA_TYPE = np.int32
FP_ARRAY_DATA_TYPE = np.float32

THRESHOLD_PERCENTILE = 40


SkaterSeasonTopResult = namedtuple('SkaterSeasonTopResult', ['type', 'pid', 'value'])


def fraction(a, b):
    res = np.divide(a, b, out=np.zeros_like(a, dtype=FP_ARRAY_DATA_TYPE), where=b != 0)
    return res if len(res.shape) > 0 else float(res)


def percentage(a, b):
    return 100 * fraction(a, b)


def stats_to_array(stats, arr_len):
    # arr_len can be more than original number of stats. Array'll have additional space for computed stats
    data = np.zeros([len(stats), arr_len], dtype=INT_ARRAY_DATA_TYPE)
    data[:, 0:len(stats[0])] = stats
    return data


def find_index(arr, value):
    # for 1D arrays ONLY
    res = np.where(arr == value)[0]
    return res[0] if len(res) > 0 else None


def find_rate(obj_row_idx, values_col, desc_order=True):
    if desc_order:
        indices = np.argsort(values_col)[::-1]
    else:
        indices = np.argsort(values_col)
    return find_index(indices, obj_row_idx) + 1


def find_rate2(obj_row_idx, values_col, threshold_col, desc_order=True):
    # This function is for relative values(like save percentage). The direct sort might be not correct.
    # We need to put much-playing players to the top of the rating.
    threshold = np.percentile(threshold_col, THRESHOLD_PERCENTILE)
    shift = 1000
    if desc_order:
        col = np.where(threshold_col > threshold, values_col + shift, values_col)
        indices = np.argsort(col)[::-1]
    else:
        col = np.where(threshold_col < threshold, values_col + shift, values_col)
        indices = np.argsort(col)
    return find_index(indices, obj_row_idx) + 1


def get_rate_and_avg(arr, column, obj_row_idx, desc_order=True):
    col = arr[:, column]
    return find_rate(obj_row_idx, col, desc_order), col.mean()


def date_to_int(date):
    return int(time.mktime(date.timetuple()))


def get_indexes_max_results(arr, column):
    value = np.max(arr[:, column])
    return np.argwhere(arr[:, column] == value).flatten()


def get_indexes_min_results(arr, column):
    value = np.min(arr[:, column])
    return np.argwhere(arr[:, column] == value).flatten()
