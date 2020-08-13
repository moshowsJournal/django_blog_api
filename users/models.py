from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, AbstractUser
from random import randint
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# Create your models here.

def upload_location(instance,filename):
    file_path = '/users/{user_id}-{full_name}-{random_number}'.format(user_id = instance.id,
    username = instance.username,random_number = randint(1000,10000))
    return file_path


class MainUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have a username')
        user = User.model(
            user = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(self._db)
        return user

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to=upload_location,null=True)

    def __str__(self):
        return '{email}-{user_id}'.format(email=self.email,user_id=self.id)

    @property
    def token(self):
        Token.objects.get(user__id=self.id)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        return Token.objects.create(user=instance)
