from django.contrib.auth import authenticate, login
from rest_framework import serializers


def get_and_authenticate_user(request, email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)

    elif user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user