from functools import wraps

import jwt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

import keys
import messages


class Helper:

    @staticmethod
    def generate_access_token(username):
        payload = {
            keys.USERNAME: username
        }
        return jwt.encode(payload, keys.JWT_SECRET, algorithm='HS256')

    @staticmethod
    def decode_access_token(request):
        try:
            access_token = request.headers[keys.ACCESS_TOKEN]
        except:
            return None

        if access_token == None:
            return None

        try:
            decoded = jwt.decode(access_token, keys.JWT_SECRET, algorithms='HS256')
            print(decoded)
            username = decoded[keys.USERNAME]
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        except jwt.exceptions.DecodeError:
            return None

    @staticmethod
    def validate_access_token(function):
        """
        Custom decorator to verify user access token
        """

        @wraps(function)
        def wrap(request, *args, **kwargs):
            res = Helper.decode_access_token(request)
            if res == None:
                return Response(data={keys.SUCCESS: False, keys.MESSAGE: messages.INVALID_TOKEN},
                                status=status.HTTP_403_FORBIDDEN)
            return function(request, *args, **kwargs)

        return wrap
