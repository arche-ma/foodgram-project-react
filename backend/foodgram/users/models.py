from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password,
                                **extra_fields)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = [(USER, 'User'),
                    (ADMIN, 'Admin')]
    role = models.CharField(verbose_name='Роль', max_length=500,
                            choices=ROLE_CHOICES, default=USER,
                            blank=False)
    email = models.EmailField(verbose_name='Адрес электронной почты',
                              unique=True)
    following = models.ManyToManyField('User', related_name='follower')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    def clean_role(self):
        if self.role not in list(zip(*self.ROLE_CHOICES))[0]:
            raise ValidationError(
                {'role': 'this role doesn\'t exist'})

    def save(self, *args, **kwargs):
        self.clean_role()
        if self.is_superuser:
            self.role = self.ADMIN
        return super().save(*args, **kwargs)
