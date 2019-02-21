from rest_framework import serializers

from .models import Profile, User


class GetProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile

        fields = (
            'username', 'bio', 'image_url',
            'company', 'website', 'location', 'phone')

        read_only_fields = ("created_at", "updated_at")


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    class Meta:
        model = Profile

        fields = ('bio', 'image_url',
                  'company', 'website',
                  'location', 'phone', 'image')

        extra_kwargs = {"image": {"write_only": True}}
        read_only_fields = ("created_at", "updated_at")

    def update(self, instance, validated_data):
        """
        Update profile function.
        """
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.company = validated_data.get('company', instance.company)
        instance.website = validated_data.get('website', instance.website)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        instance.image_url = instance.image.url
        instance.save()

        return instance


class FollowerFollowingSerializer(serializers.ModelSerializer):
    """Serializer that return username"""
    class Meta:
        model = User
        fields = ('username', )


class FollowUnfollowSerializer(serializers.ModelSerializer):
    """Serializer that returns id, username, followers, following"""

    followers_total = serializers.SerializerMethodField()
    following_total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'followers_total', 'following_total',
        )

    def get_followers_total(self, obj):
        """Returns total number of followers"""
        return obj.followers.count()

    def get_following_total(self, obj):
        """Returns number of users one is following"""
        return obj.following.count()
