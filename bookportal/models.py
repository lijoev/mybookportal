from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    """
    Profile model to save user profile linked to Auth user by onetoone field.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500)
    about = models.CharField(max_length=1000)
    slogan = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username


class Books(models.Model):
    """Books model which shows basic book details."""

    CATEGORY_CHOICES = (
        ("HE", "Health"),
        ("SOC", "Social"),
        ("MA", "Music & Audio"),
        ("PT", "Programming & Tech")
    )

    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500, default="lijo")
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    cover = models.FileField(upload_to='books')
    file = models.FileField(upload_to='files', default='settings.MEDIA_ROOT/files/resume.pdf')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    """
    model to save the purchases of the user
    """
    book = models.ForeignKey(Books)
    buyer = models.ForeignKey(User)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.book.title


class Review(models.Model):
    """
    model to save the review against a book
    """
    book = models.ForeignKey(Books)
    user = models.ForeignKey(User)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content
