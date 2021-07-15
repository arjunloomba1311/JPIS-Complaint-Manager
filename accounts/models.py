from django.db import models

from django.db import models
# Create your models here.
from django.contrib.auth.models import User

#extending the original django user model
class user_profile(models.Model):
    hunter = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    grade = models.CharField(max_length=3)
    is_admin = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)

    def __str__(self):
        return self.hunter.username

# Create your models here.
