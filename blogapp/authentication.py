import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed


def generate_jwt_token(user):
    """
    Generates a JWT token.
    """
    payload = {
        'id': user.pk,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=360),  # Token expiration time
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    return token


def authenticate_user(username, password):
    """
    Authenticates the user and returns a JWT token if successful.
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        token = generate_jwt_token(user)
        return token
    return None


def decode_jwt_token(token):
    """
    Decodes the JWT token and returns the user if the token is valid.
    """
    try:
        payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        user = User.objects.get(id=payload['id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        raise AuthenticationFailed('Invalid or expired token')


def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('token')

        if not token:
            raise AuthenticationFailed('Token is missing')

        try:
            user = decode_jwt_token(token)  # Decode token and validate
            request.user = user  # Attach user to request
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        return view_func(request, *args, **kwargs)
    return wrapper
