from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.
def image1_path(self, filename):
    return "images/devices/{}/1/".format(self.title)

def image2_path(self, filename):
    return "images/devices/{}/2/".format(self.title)

def image3_path(self, filename):
    return "images/devices/{}/3/".format(self.title)

def image4_path(self, filename):
    return "images/devices/{}/4/".format(self.title)

class Device(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField()
    img1 = models.ImageField(upload_to=image1_path, null=False, blank=False)
    img2 = models.ImageField(upload_to=image2_path)
    img3 = models.ImageField(upload_to=image3_path)
    img4 = models.ImageField(upload_to=image4_path)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
