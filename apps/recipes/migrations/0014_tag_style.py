# Generated by Django 3.2 on 2021-04-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='style',
            field=models.CharField(default='orange', max_length=50, verbose_name='Css постфикс тэга'),
        ),
    ]