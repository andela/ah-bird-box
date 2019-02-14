from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from authors.apps.authentication.models import User


# Create your models here.
class Profile(models.Model):
    """
    create a user profile model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image_url = CloudinaryField(
        "image",
        default="https://res.cloudinary.com/dy2faavdk/image/upload/v1548264034/qvxtpdmi03kksg9rxgfj.png")  # noqa

    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=100, blank=True)
    location = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    create profile upon user registration.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save created user profile.
    """
    instance.profile.save()
