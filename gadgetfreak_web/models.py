from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver

from django.contrib.auth.models import User

# Create your models here.
def image1_path(self, filename):
    return "images/devices/{}/1".format(self.title)

def image2_path(self, filename):
    return "images/devices/{}/2".format(self.title)

def image3_path(self, filename):
    return "images/devices/{}/3".format(self.title)

def image4_path(self, filename):
    return "images/devices/{}/4".format(self.title)

def image_thumb_path(self, filename):
    return "images/devices/{}/thumb".format(self.title)

class Device(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField()
    img_1 = models.ImageField(upload_to=image1_path, null=False, blank=False)
    img_2 = models.ImageField(upload_to=image2_path, null=True, blank=True)
    img_3 = models.ImageField(upload_to=image3_path, null=True, blank=True)
    img_4 = models.ImageField(upload_to=image4_path, null=True, blank=True)
    img_thumb = models.ImageField(upload_to=image_thumb_path, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

@receiver(models.signals.post_save, sender=Device)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        print("create!")