from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follower(models.Model):
    followed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'followed_by'
    )
    following = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )