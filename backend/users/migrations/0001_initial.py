# Generated by Django 3.2.18 on 2023-04-11 08:46

import core.limits
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(help_text='Обязательно для заполнения', max_length=core.limits.Limits['LEN_EMAIL_LIMIT'], unique=True, verbose_name='Адрес электронной почты')),
                ('username', models.CharField(help_text='Обязательно для заполнения', max_length=core.limits.Limits['LEN_USERS_NAME_LIMIT'], unique=True, verbose_name='Юзернейм')),
                ('first_name', models.CharField(help_text='Обязательно для заполнения', max_length=core.limits.Limits['LEN_USERS_NAME_LIMIT'], verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Обязательно для заполнения', max_length=core.limits.Limits['LEN_USERS_NAME_LIMIT'], verbose_name='Фамилия')),
                ('password', models.CharField(help_text='Обязательно для заполнения', max_length=core.limits.Limits['LEN_USERS_NAME_LIMIT'], verbose_name='Пароль')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активирован')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
    ]
