from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='user')
    lang = models.CharField(max_length=2,
                            choices=[('ru', 'Русский'), ('en', 'Английский')],
                            default='ru')
    theme = models.CharField(max_length=5,
                             choices=[('light', 'Светлая'), ('dark', 'Темная')],
                             default='light')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class City(models.Model):
    City = models.CharField(max_length=100)
    Temperature = models.CharField(max_length=100)
    Weather = models.TextField()

    def __str__(self):
        return self.City

class PDFFile(models.Model):
    name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=50)
    file_data = models.BinaryField()

    def __str__(self):
        return self.name