# Generated by Django 3.2.18 on 2023-04-17 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230417_1545'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_relationships',
        ),
        migrations.RemoveConstraint(
            model_name='subscription',
            name='prevent_self_follow',
        ),
    ]
