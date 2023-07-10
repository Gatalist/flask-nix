from marshmallow import Schema, validate, fields


class MoviesSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    poster = fields.String()
    reliase = fields.Str()
    director = fields.String()
    rating = fields.Str()
    user_id = fields.Integer(dump_only=True)
    genres = fields.List(fields.String())

