from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_editable', False) # superuser data can't be edited

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=150, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    contact_no = models.CharField(max_length=20)
    # phone_number = models.CharField(max_length=20)

    user_type = models.IntegerField(null=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_employee= models.BooleanField(default=False)
    status= models.IntegerField(default=1)
    is_editable = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]

    def __str__(self):
        return self.email
