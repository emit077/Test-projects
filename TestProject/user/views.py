# Create your views here.
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import keys
import messages
from helper import Helper
from .models import UserData


@api_view(['POST'])
def signup(request):
    """
    params:
    mobile -- required
    password -- required
    gender -- required
    city -- required
    state -- required
    """
    print(request.data)
    username = request.data.get(keys.USERNAME, None)
    email = request.data.get(keys.EMAIL, None)
    password = request.data.get(keys.PASSWORD, None)
    gender = request.data.get(keys.GENDER, None)
    city = request.data.get(keys.CITY, None)
    state = request.data.get(keys.STATE, None)

    if User.objects.filter(username=username).exists():
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.USER_NAME_ALREADY_EXIST
        }, status=status.HTTP_200_OK)

    """ crating the user object """
    user = User.objects.create(
        username=username,
        email=email,
    )
    user.set_password(password)
    user.save()
    try:
        UserData.objects.create(
            auth_user=user,
            gender=gender,
            city=city,
            state=state,
        )
    except Exception as e:
        print("Error while creating userdata", str(e))
        user.delete()

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.USERNAME: user.username,
    }
    headers = {
        keys.ACCESS_TOKEN: Helper.generate_access_token(user.username)
    }
    return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
def login(request):
    """
        username -- mobile number is required
        password -- password is required
    """
    username = request.data.get(keys.USERNAME, None)
    password = request.data.get(keys.PASSWORD, None)

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.INVALID_USERNAME
        }, status=status.HTTP_200_OK)

    print(check_password(password, user.password))
    if not check_password(password, user.password):
        return Response({
            keys.SUCCESS: False,
            keys.MESSAGE: messages.INVALID_CREDENTIALS
        }, status=status.HTTP_200_OK)

    else:
        response = {
            keys.SUCCESS: True,
            keys.MESSAGE: messages.SUCCESS,
            keys.USERNAME: user.username,
        }
        headers = {
            keys.ACCESS_TOKEN: Helper.generate_access_token(user.username)
        }

        return Response(response, status=status.HTTP_200_OK, headers=headers)


@api_view(['GET'])
@Helper.validate_access_token
def home(request):
    user = Helper.decode_access_token(request)

    response = {
        keys.SUCCESS: True,
        keys.MESSAGE: messages.SUCCESS,
        keys.USERNAME: user.username,
    }
    return Response(response, status=status.HTTP_200_OK)
