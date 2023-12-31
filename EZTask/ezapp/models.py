from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    #username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    #password = models.CharField(max_length=200)
    uutoken=models.CharField(max_length=100,null=True,blank=True)
    loginToken = models.CharField(max_length=500)

    def __str__(self):
        return self.username