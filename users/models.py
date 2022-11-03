from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    profile_pix = models.ImageField(null=True, blank=True, upload_to='profile')

    def __str__(self):
        return self.fullname


