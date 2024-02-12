from django.contrib import admin

# Register your models here.
from .models import Follower

class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower,FollowerAdmin)