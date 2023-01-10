from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from users.managers import MclUserManager

class MclUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    mcl_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MclUserManager()

    def __str__(self):
        return self.email

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(MclUser, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user.username

class Student(Person):
    section_ID = models.ForeignKey("visualizer.Section", on_delete=models.PROTECT)
    strand_ID = models.ForeignKey("visualizer.Strand", on_delete=models.PROTECT)

class Teacher(Person):
    pass

class Principal(Person):
    pass