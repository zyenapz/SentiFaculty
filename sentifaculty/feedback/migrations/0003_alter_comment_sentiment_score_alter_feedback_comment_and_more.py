# Generated by Django 4.1.4 on 2023-01-26 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='sentiment_score',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='feedback.sentimentscore'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='feedback.comment'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='evaluatee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='feedback.evaluatee'),
        ),
    ]