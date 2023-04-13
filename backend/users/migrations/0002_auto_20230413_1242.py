# Generated by Django 3.2.18 on 2023-04-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_subscribed',
            field=models.BooleanField(default=False, help_text='Отметьте для подписки на данного пользователя', verbose_name='Подписан ли текущий пользователь на этого'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
