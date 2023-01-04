# Generated by Django 4.1.4 on 2023-01-03 08:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.TextField(max_length=100, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]