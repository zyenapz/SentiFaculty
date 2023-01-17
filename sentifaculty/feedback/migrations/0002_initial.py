# Generated by Django 4.1.4 on 2023-01-17 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('feedback', '0001_initial'),
        ('visualizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='evaluatee',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.subject'),
        ),
        migrations.AddField(
            model_name='evaluatee',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher'),
        ),
    ]
