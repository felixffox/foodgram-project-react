from core.limits import Limits
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=Limits.LEN_EMAIL_LIMIT,
        unique=True,
        help_text='Обязательно для заполнения'
    )
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=Limits.LEN_USERS_NAME_LIMIT,
        unique=True,
        help_text='Обязательно для заполнения'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=Limits.LEN_USERS_NAME_LIMIT,
        help_text='Обязательно для заполнения'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=Limits.LEN_USERS_NAME_LIMIT,
        help_text='Обязательно для заполнения'
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=Limits.LEN_USERS_PASSWORD_LIMIT,
        help_text='Обязательно для заполнения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}: {self.email}'


class Subscriptions(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='subscribers',
        to=MyUser,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Подписчик',
        related_name='subscriptions',
        to=MyUser,
        on_delete=models.CASCADE,
    )
    subscription_date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            UniqueConstraint(
                fields=('author', 'user'),
                name='\nRepeat subscription\n',
            ),
            CheckConstraint(
                check=~Q(author=F('user')),
                name='\nNo self sibscription\n'
            )
        )

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.author.username}'