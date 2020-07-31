from django.contrib import admin
from .models import Post, Comment,Preference

# Register your models here.
admin.site.register([Post, Comment,Preference])
