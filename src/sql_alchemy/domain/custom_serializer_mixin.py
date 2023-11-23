from datetime import timedelta
from sqlalchemy_serializer import SerializerMixin


def serialize_timedelta(value: timedelta):
    return value.total_seconds()


class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (timedelta, serialize_timedelta),
    )
