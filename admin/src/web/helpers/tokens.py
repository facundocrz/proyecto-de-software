from flask import current_app
from itsdangerous.url_safe import URLSafeSerializer


_serializers = {}


def get_serializer(name):
    serializer = _serializers.get(name)
    if serializer is None:
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'], salt=name)
        _serializers[name] = serializer

    return serializer