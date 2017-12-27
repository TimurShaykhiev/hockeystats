import numpy as np

INT_ARRAY_DATA_TYPE = np.int32
FP_ARRAY_DATA_TYPE = np.float32


def fraction(a, b):
    res = np.divide(a, b, out=np.zeros_like(a, dtype=FP_ARRAY_DATA_TYPE), where=b != 0)
    return res if len(res.shape) > 0 else float(res)


def percentage(a, b):
    return 100 * fraction(a, b)


def stats_to_array(stats, arr_len):
    # arr_len can be more than original number of stats. Array'll have additional space for computed stats
    data = np.zeros([len(stats), arr_len], dtype=INT_ARRAY_DATA_TYPE)
    data_iter = data.flat
    idx = 0
    for st in stats:
        # remove season info from stats
        data_iter[idx] = st[0]  # object id
        data_iter[idx + 1:idx + len(st) - 2] = st[3:]  # object stats
        idx += arr_len
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


def get_rate_and_avg(arr, column, obj_row_idx, desc_order=True):
    col = arr[:, column]
    return find_rate(obj_row_idx, col, desc_order), col.mean()
