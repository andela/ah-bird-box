from rest_framework import serializers

from .models import Profile


class GetProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile

        fields = ('username', 'bio', 'image_url', 'company', 'website', 'location', 'phone')  # noqa

        read_only_fields = ("created_at", "updated_at")


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    class Meta:
        model = Profile

        fields = ('bio', 'image_url', 'company', 'website', 'location', 'phone')  # noqa
        read_only_fields = ("created_at", "updated_at")

    def update(self, instance, validated_data):
        """
        Update profile function.
        """
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image_url', instance.image_url)
        instance.company = validated_data.get('company', instance.company)
        instance.website = validated_data.get('website', instance.website)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        instance.image_url = instance.image_url.url
        instance.save()

        return instance
