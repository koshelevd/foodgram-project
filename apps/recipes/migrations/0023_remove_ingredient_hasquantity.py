# Generated by Django 3.2 on 2021-04-21 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0022_auto_20210421_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='hasQuantity',
        ),
    ]