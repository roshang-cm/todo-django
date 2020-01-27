from django.db import models
from todo.managers import UserProfileManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from todo.constants import STATUS_CHOICES
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class UserProfile(AbstractBaseUser, BaseModel, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        unique=True
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserProfileManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'UserProfile[{self.pk}](Username={self.username})'


class Todo(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(
        default=STATUS_CHOICES[0][0],
        max_length=10,
        choices=STATUS_CHOICES)

    def __str__(self):
        return f'Todo[{self.pk}](Text={self.text}, Status={self.status}, User={self.user.username})'
