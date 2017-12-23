# Models in this package represent objects returned by API.
from marshmallow import Schema, fields
import numpy as np


class ModelSchema(Schema):
    def dumps(self, obj, many=None, update_fields=True, *args, **kwargs):
        return super().dumps(obj, many, update_fields, *args, **dict(kwargs, separators=(',', ':')))


class StatValue(fields.Number):
    def _serialize(self, value, attr, obj):
        val_type = type(value)
        if val_type == int or val_type == np.int32 or val_type == np.int64:
            self.num_type = int
        else:
            self.num_type = float
        return super()._serialize(value, attr, obj)
