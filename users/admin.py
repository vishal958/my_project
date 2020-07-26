from django.contrib import admin
from .models import Profile, balance

# Register your models here.
admin.site.register([Profile, balance])
