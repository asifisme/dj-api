from django.contrib.auth.models import BaseUserManager  


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for User model
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email and password
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)