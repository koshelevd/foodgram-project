# Generated by Django 3.2 on 2021-04-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredient_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='hasQuantity',
            field=models.SlugField(default=True, null=True, verbose_name='Содержит количество'),
        ),
    ]