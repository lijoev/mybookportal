from django.contrib import admin
from .models import Profile, Books, Purchase, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Books)
admin.site.register(Purchase)
admin.site.register(Review)
