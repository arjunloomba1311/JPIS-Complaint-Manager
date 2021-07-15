from django.db import models

from django.contrib.auth.models import User


class complaint_info(models.Model):
    title = models.TextField(max_length = 100)
    pub_date = models.DateTimeField()
    description = models.TextField()
    room_no = models.IntegerField()
    image = models.ImageField(upload_to = 'images/')
    hunter = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    approved = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)
    pending = models.BooleanField(default = True)
    mail_sent = models.BooleanField(default = False)
    issue_type = models.IntegerField(default = 1)
    rating = models.IntegerField(default = 5)
    fixed = models.BooleanField(default = False)
    cost = models.IntegerField(default = 5)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title

    def description_short(self):
        return self.description[:75]

class admin_complaints(models.Model):
    complaints = models.OneToOneField(complaint_info, on_delete = models.CASCADE, null = True)



#if current doesnt work - make new class for approved and rejected
