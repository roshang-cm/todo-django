from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, username, password, **extras):
        user = self.model(username=username, **extras)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extras):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)
        return self.create_user(username, password, **extras)
