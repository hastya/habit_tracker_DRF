from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

NULLABLE = {'blank':  True, 'null': True}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='E-mail')
    telegram = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Telegram', **NULLABLE)

    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона', **NULLABLE)
    is_active = models.BooleanField(verbose_name='Активность', default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
