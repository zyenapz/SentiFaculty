from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.managers import MclUserManager

# User Type - choices
STUDENT = 1
TEACHER = 2
PRINCIPAL = 3
ADMIN = 4
USER_TYPE_CHOICE = (
    (STUDENT, 'student'),
    (TEACHER, 'teacher'),
    (PRINCIPAL, 'principal'),
    (ADMIN, 'admin'),
)


class MclUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    mcl_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICE, default=STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MclUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        # TODO Before changing user type, validate first if a Person sub-class is already set for the MclUser
        # NOTE (Current) Another solution is just don't allow the user_type to be modified after creation
        pass

class Person(models.Model):
    user = models.OneToOneField(MclUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Student(Person):
    section_ID = models.ForeignKey("visualizer.Section", on_delete=models.PROTECT)
    strand_ID = models.ForeignKey("visualizer.Strand", on_delete=models.PROTECT)

    def clean(self):
        if self.user.user_type != STUDENT:
            raise ValidationError("User must be a Student.")

class Teacher(Person):
    def clean(self):
        if self.user.user_type != TEACHER:
            raise ValidationError("User must be a Teacher.")

class Principal(Person):
    def clean(self):
        if self.user.user_type != PRINCIPAL:
            raise ValidationError("User must be a Principal.")