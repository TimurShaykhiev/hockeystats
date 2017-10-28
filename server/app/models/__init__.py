# Models in this package represent objects returned by API.
from marshmallow import Schema


class ModelSchema(Schema):
    def dumps(self, obj, many=None, update_fields=True, *args, **kwargs):
        return super().dumps(obj, many, update_fields, *args, **dict(kwargs, separators=(',', ':')))
