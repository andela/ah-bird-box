from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import (
    UpdateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# local imports
from .models import Profile
from .serializers import (
    GetProfileSerializer, UpdateProfileSerializer,
    FollowerFollowingSerializer, FollowUnfollowSerializer)
from .renderers import ProfileJSONRenderer
from .models import User


class ListProfileView(RetrieveAPIView):
    """
    Permitted users view their profile and other profiles.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = GetProfileSerializer

    def get_queryset(self):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=self.kwargs.get('username')
            )
            return profile
        except Exception:

            raise NotFound('Requested profile not found')

    def retrieve(self, request, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, context={'request': request})

        return Response(serializer.data)


class AuthorsProfileListAPIView(ListAPIView):
    """
    Views a list of authors profiles
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = GetProfileSerializer
    queryset = Profile.objects.all()


class EditUserProfileView(UpdateAPIView):
    """
    a user can edit his own profile but cannot another user's profile
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.select_related('user').get(
            user__username=self.request.user.username
        )
        return obj

    def put(self, request, username):
        if request.user.username != username:
            raise PermissionDenied('Edit permission denied')

        else:

            return super().put(request, username)


class FollowUnfollowAPIView(RetrieveUpdateDestroyAPIView):
    """
    APIView for following a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        """
        This method create a user relationship btween the user
        with the username passed in and the user sending the
        request
        """
        try:
            to_be_followed = User.objects.get(username=username)
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if request.user == to_be_followed:
            message = {
                "error": "You cannot follow yourself"
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            user = User.objects.get(email=request.user)
            already_followed = user.following.filter(
                username=username).exists()
            if already_followed:
                return Response({
                    'error': f'You already follow {username}'
                },
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({
                'error': 'Error when following',
                'message': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.user.following.add(to_be_followed)
        request.user.save()

        serializer = FollowUnfollowSerializer(request.user)
        message = {
            "message": f"You are now following {username}",
            "user": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, username, format=None):
        """
        Deletes a follow relationship between the user sending the
        request and the user with the username passed
        """
        try:
            id = User.objects.get(username=username).id
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        follower = User.objects.get(pk=request.user.id)

        relationship = follower.following.filter(pk=id).exists()
        if not relationship:
            return Response(
                {
                    'error': f'You do not follow {username}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        follower.following.remove(id)
        serializer = FollowUnfollowSerializer(follower)
        message = {
            "message": f"You have successfully unfollowed {username}",
            "user": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)


class FollowerFollowingAPIView(ListAPIView):
    """
    This API returns a list of user followers and following
    """

    def get_queryset(self):
        user = get_object_or_404(
            User, id=User.objects.get(username=self.kwargs['username']).id)

        followed_friends = user.following.all()
        following_friends = user.followers.all()

        return {
            "followed": followed_friends,
            "followers": following_friends
        }

    def get(self, request, username, format=None):
        """Returns the user's followed user"""
        if self.get_queryset() is not None:

            following_dict = self.get_queryset()

            follower_serializer = FollowerFollowingSerializer(
                following_dict['followed'], many=True)
            following_serializer = FollowerFollowingSerializer(
                following_dict['followers'], many=True)

            message = {
                "message": f"{username}'s statistics:",
                "Followers": follower_serializer.data,
                "Following": following_serializer.data
            }
            return Response(message, status=status.HTTP_200_OK)
