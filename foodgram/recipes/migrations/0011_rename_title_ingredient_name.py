# Generated by Django 3.2 on 2021-04-12 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_ingredient_hasquantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='title',
            new_name='name',
        ),
    ]
