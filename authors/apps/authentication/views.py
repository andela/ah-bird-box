from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .models import User
from .helper_functions.send_email import send_email
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    SocialAuthSerializer, PasswordResetSerializer
)
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
from rest_framework.generics import (RetrieveUpdateAPIView, CreateAPIView,
                                     UpdateAPIView)
from .backends import JWTAuthentication


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialAuthView(CreateAPIView):
    """Login via social sites (Google, Facebook)"""
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """Takes in provider and access_token to authenticate user"""
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider")
        authenticated_user = request.user if not request.user.is_anonymous else None # noqa E501
        strategy = load_strategy(request)

        # Load backend associated with the provider
        try:

            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)
            if isinstance(backend, BaseOAuth1):
                if "access_token_secret" in request.data:
                    access_token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret': request.data['access_token_secret'] # noqa E501
                    }
                else:
                    return Response(
                        {"error": "Access token secret is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            elif isinstance(backend, BaseOAuth2):

                access_token = serializer.data.get("access_token")

        except MissingBackend:
            return Response({"error": "The Provider is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Go through the pipeline to create user if they don't exist
        try:
            user = backend.do_auth(access_token, user=authenticated_user)

        except BaseException:
            return Response({"error": "Invalid token"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:

            email = user.email
            username = user.username
            token = user.token
            user_data = {
                "username": username,
                "email": email,
                "token": token
            }
            return Response(user_data, status=status.HTTP_200_OK)


class PasswordResetAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        recipient = request.data.get('email', {})  # user enters email
        if not recipient:
            return Response({"message": "Please provide an email address"},
                            status=status.HTTP_400_BAD_REQUEST)

        # confirm if user exists and generate a token for email entered
        user = User.objects.filter(email=recipient).exists()
        if user:
            user = User.objects.get(email=recipient)
            token = user.token
            result = send_email(recipient, token, request)
            return Response(result, status=status.HTTP_200_OK)
        else:  # if user does not exist
            result = {
                'message': 'Sorry, user with this email does not exist'
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)


class PasswordUpdateAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({"message": "Sorry, your passwords do not match"},
                            status=status.HTTP_400_BAD_REQUEST)
        password = {
            "password": password
        }
        serializer = self.serializer_class(data=password)
        serializer.is_valid(raise_exception=True)

        try:
            user_email, token = JWTAuthentication.authenticate_token(self, request, token) # noqa 
            user = User.objects.get(email=user_email)
            user.set_password(request.data.get('password'))
            user.save()
            result = {'message': 'Your password has been reset successfully'}
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
