# Generated by Django 3.2 on 2021-04-20 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_follow'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='follow',
            name='author',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]