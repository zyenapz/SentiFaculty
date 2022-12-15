from django.contrib.auth.models import User
from django.db import models


class Teacher(models.Model):
    # NOTE we are extending User via a OneToOneField: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-user
    # the ERD makes use of a Teacher ID as primary key
    # need to test if the id is automatically generated
    # (models with no specified primary key usually do)
    # NOTE extending User like this is completely unnecessary
    # but our ERD defines a Teacher entity, so there will be a discrepancy if we do not
    # have it in our model, we can remove this if we want to
    # the Teacher entity also has a teacher ID, which is why I opted not to use a proxy model
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Subject(models.Model):
    teacher_ID = models.ForeignKey(Teacher, on_delete=models.PROTECT)
