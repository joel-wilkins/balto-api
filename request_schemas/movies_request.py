from marshmallow import Schema, fields


class MoviesRequest(Schema):
    page = fields.Int(missing=1)
    page_size = fields.Int(missing=100)


class GenreRequest(Schema):
    id = fields.UUID()
    genre = fields.Str()


class OriginRequest(Schema):
    id = fields.UUID()
    origin = fields.Str()


class MovieCastRequest(Schema):
    id = fields.UUID()
    first_name = fields.Str()
    last_name = fields.Str()
    full_name = fields.Str()


class MovieDirectorRequest(Schema):
    id = fields.UUID()
    first_name = fields.Str()
    last_name = fields.Str()
    full_name = fields.Str()


class MovieUpsertRequest(Schema):
    id = fields.Str()
    release_year = fields.Int(required=True)
    title = fields.Str(required=True)
    wikipedia_link = fields.Str(required=True)
    plot = fields.Str(required=True)
    cast = fields.Nested(MovieCastRequest(many=True))
    directors = fields.Nested(MovieDirectorRequest(many=True))
    origin = fields.Nested(OriginRequest)
    genre = fields.Nested(GenreRequest)
