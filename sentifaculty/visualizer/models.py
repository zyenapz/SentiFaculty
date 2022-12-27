from django.contrib.auth.models import User
from django.db import models


class Teacher(models.Model):
    # NOTE we are extending User via a OneToOneField: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-user
    # NOTE extending User like this is completely unnecessary
    # but our ERD defines a Teacher entity, so there will be a discrepancy if we do not
    # have it in our model, we can remove this if we want to
    # the Teacher entity also has a teacher ID, which is why I opted not to use a proxy model
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user.username


class Subject(models.Model):
    teacher_ID = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    subject_name=models.CharField(max_length=250,default='subj')

    def __str__(self) -> str:
        return self.subject_name