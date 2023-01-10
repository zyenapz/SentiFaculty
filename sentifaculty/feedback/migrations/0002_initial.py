# Generated by Django 4.1.4 on 2023-01-10 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('visualizer', '0001_initial'),
        ('feedback', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.academicyear'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='sentiment_score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.sentimentscore'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher'),
        ),
    ]
