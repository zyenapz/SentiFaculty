# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Teacher

# @receiver(post_save, sender=User)
# def create_teacher(sender, instance, created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_teacher(sender, instance, **kwargs):
#     instance.teacher.save()