import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    """
    This class handles authentication of the user.
    """

    def authenticate(self, request):
        """This method authenticates the Authorization header
        GIVEN:
            request (Request object): Django Request context
        RETURN:
            None: Failed Authentication
            (user, token): Successful Authentication.
        """

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) < 2:
            msg = 'Invalid authorization header'
            raise exceptions.AuthenticationFailed(msg)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != 'Bearer':
            msg = 'Use a Bearer Token'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_token(request, token)

    def authenticate_token(self, request, token):
        """This method authenticates the given token
        GIVEN:
            request (Request object): Django Request context
            token (str): JSON Web Token
        RETURN:
            None: Failed Authentication
            (user, token): Successful Authentication.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Token decode failed'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignatureError:
            msg = 'Token expired, please re-authenticate.'
            raise exceptions.AuthenticationFailed(msg)

        email = payload['user_data']['email']
        username = payload['user_data']['username']

        try:
            user = User.objects.get(email=email, username=username)

        except User.DoesNotExist:
            msg = 'No user matching this token'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User has been deactivated"
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
