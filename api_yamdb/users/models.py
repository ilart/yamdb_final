import enum

from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Переопределенный обьект класса Пользователь"""
    class Roles(enum.Enum):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    email = models.EmailField(
        'Почта',
        max_length=254,
    )
    role = models.CharField(
        'Роль',
        choices=ROLES,
        default='user',
        max_length=32
    )
    bio = models.CharField(
        max_length=512,
        blank=True,
    )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.Roles.admin.value

    @property
    def is_user(self):
        return self.role == self.Roles.user.value

    @property
    def is_moderator(self):
        return self.role == self.Roles.moderator.value

    def __str__(self):
        return self.username
