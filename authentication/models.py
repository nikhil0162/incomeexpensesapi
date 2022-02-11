from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from helpers.models import TimestampModel
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise ValueError('username must not be blank.')
        if email is None:
            raise ValueError('email must not be blank.')

        user_obj = self.model(username=username, email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_superuser(self, username, email, password,**extra_kwargs):        
        if password is None:
            raise ValueError('password must not be None')

        user_obj = self.create_user(username, email, password)
        user_obj.is_superuser = True
        user_obj.is_staff = True
        user_obj.is_active = True
        user_obj.save()
        return user_obj


class User(AbstractBaseUser, PermissionsMixin,TimestampModel):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
