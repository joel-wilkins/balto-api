from marshmallow import Schema, fields


class MoviesRequest(Schema):
    page = fields.Int(missing=1)
    page_size = fields.Int(missing=100)
