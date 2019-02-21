from django.db import models
from django.utils.text import slugify

from authors.apps.authentication.models import User
from cloudinary.models import CloudinaryField


class Article(models.Model):
    """
    The model for creating the articles is defined here
    """
    slug = models.SlugField(
        db_index=True, max_length=1000, unique=True, blank=True)
    title = models.CharField(max_length=1000, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    body = models.TextField(blank=False)
    image_url = CloudinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(
        User, related_name='article', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(
        User, related_name='likes', blank=True)
    disliked_by = models.ManyToManyField(
        User, related_name='dislikes', blank=True)
    tags = models.ManyToManyField('articles.Tag', related_name='articles')

    def __str__(self):
        return self.title

    def create_slug(self):
        """
        Convert title to slug
        If the title exists, append an integer to differentiate the slug
        """
        slug = slugify(self.title)
        new_slug = slug
        n = 1
        while Article.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(slug, n)
            n += 1

        return new_slug

    def save(self, *args, **kwargs):
        """
        Article saved after creating slug
        """
        if not self.slug:
            self.slug = self.create_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    """
    The model for creating tags for Articles
    """
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag
