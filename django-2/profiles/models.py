from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "profiles"
    )
    image = ImageField(upload_to = 'profiles')
    
    def __str__(self) -> str:
        return self.user.username

@receiver(post_save,sender=User)
def create_user_profile(sender, instance,created,**kwargs):
    """Create a new Profile() oject when a Djago.User.is.created."""
    if created:
        Profile.objects.create(user=instance)
