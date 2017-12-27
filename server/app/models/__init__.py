# Models in this package represent objects returned by API.
from flask import request
from marshmallow import Schema, fields
import numpy as np

from app.api.response_utils import InvalidQueryParams


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


def get_locale():
    locale_query_param = 'locale'
    default_locale = 'en'
    supported_locales = ['en', 'ru']
    locale = request.args.get(locale_query_param, type=str)
    if locale is None:
        raise InvalidQueryParams()

    if locale in supported_locales:
        return locale
    return default_locale
