# Generated by Django 4.1.4 on 2023-01-04 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_rename_academic_year_id_feedback_acadyear_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='acadyear',
            new_name='academic_year_ID',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='bert',
            new_name='bert_ID',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='author',
            new_name='student_ID',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='teacher',
            new_name='teacher_ID',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='vader',
            new_name='vader_ID',
        ),
    ]
