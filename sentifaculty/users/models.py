from django.db import models
from django.contrib.auth.models import User

from visualizer.models import Section, Strand

# Create your models here.
class Person(models.Model):
    
    __ID_MAX_LENGTH = 10

    # NOTE we are extending User via a OneToOneField: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-user
    # NOTE extending User like this is completely unnecessary
    # but our ERD defines a Teacher entity, so there will be a discrepancy if we do not
    # have it in our model, we can remove this if we want to
    # the Teacher entity also has a teacher ID, which is why I opted not to use a proxy model
    person_ID = models.CharField(max_length=__ID_MAX_LENGTH, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    email = models.EmailField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.user.username


class Student(Person):
    pass
    # section_ID = models.ForeignKey(
    #     Section,
    #     on_delete=models.PROTECT
    # )
    # strand_ID = models.ForeignKey(Strand, on_delete=models.PROTECT)

class Teacher(Person):
    pass

class Principal(Person):
    pass