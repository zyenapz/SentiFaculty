from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    
    __ID_MAXLEN = 10

    # NOTE we are extending User via a OneToOneField: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-user
    # NOTE extending User like this is completely unnecessary
    # but our ERD defines a Teacher entity, so there will be a discrepancy if we do not
    # have it in our model, we can remove this if we want to
    # the Teacher entity also has a teacher ID, which is why I opted not to use a proxy model
    person_ID = models.CharField(max_length=__ID_MAXLEN, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.user.username

class Student(Person):
    section_ID = models.ForeignKey("visualizer.Section", on_delete=models.PROTECT)
    strand_ID = models.ForeignKey("visualizer.Strand", on_delete=models.PROTECT)

class Teacher(Person):
    pass

class Principal(Person):
    pass