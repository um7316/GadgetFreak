from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver

from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

def profile_img_path(self, filename):
    return "images/profiles/{}/{}".format(self.user.username, filename)

class UserProfile(models.Model):
    """Model representing user profle

    Model contains user profile image and is connected by one to one relationship
    with the User module from django authentication system.
    """
    user = models.OneToOneField(User, related_name="profile")
    profile_img = models.ImageField(upload_to=profile_img_path, null=False, blank=False)

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
    """Model representing the device

    Model contains title, description, four images and author of the device.
    Title must be unique, description and first image (main image) is mandatory.
    Author field is not mandatory, but should be null only, if author is deleted.
    """
    title = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField()
    img_1 = models.ImageField(upload_to=image1_path, null=False, blank=False)
    img_2 = models.ImageField(upload_to=image2_path, null=True, blank=True)
    img_3 = models.ImageField(upload_to=image3_path, null=True, blank=True)
    img_4 = models.ImageField(upload_to=image4_path, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def get_score(self):
        """Returns score fo the device

        Score is calculated by averaging all review scores, made for the device.
        If no reviews are present for the device, the score rturned is 0.
        """
        q = ForumTopic.objects.filter(topic_type="R", device_id=self.id)
        if q.count() == 0:
            return 0

        total = sum(res.score for res in q)

        return total / q.count()

    def get_no_reviews(self):
        """Returns number of reviews, made for the device
        """
        return ForumTopic.objects.filter(topic_type="R", device_id=self.id).count()

    def get_no_comments(self):
        """Returns number of reviews, made for the device
        """
        return ForumTopic.objects.filter(topic_type="C", device_id=self.id).count()

@receiver(models.signals.post_save, sender=Device)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        #print("create!")
        pass

class TechnicalSpecification(models.Model):
    """Model representing technical specificaton of a device

    It contains fields name, value and foreign key device. All fields are
    mandatory. If device is deleted, technical specifications are deleted too.
    """
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

def topic_img_path(self, filename):
    return "images/devices/{}/reviews/{}".format(self.device.title, filename)

class ForumTopic(models.Model):
    """Model representing forum topic of the device.

    It contains foreign key device. If device is deleted, topic is also deleted.
    It also contains foreign key author, connected to User model of django auth system.
    It also contains field name, topic_type, whick should be one of the 'R' or 'C', for
    review and comment, in that order. Contents field is required for both topic types.
    If topic typ is review, fields image, and score should also be present. Field date
    is automatically set to the creation date.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    REVIEW_TYPE = "R"
    COMMENT_TYPE = "C"
    TYPE_CHOICES = (
        (REVIEW_TYPE, "Review"),
        (COMMENT_TYPE, "Comment")
    )
    topic_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=COMMENT_TYPE)

    image = models.ImageField(upload_to=topic_img_path, null=True, blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    contents = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_no_comments(self):
        """Returns number of comments, made for this topic.
        """
        return Comment.objects.filter(forum_topic_id=self.id).count()

class Comment(models.Model):
    """Model, representing comment on the forum topic

    Field comtents is mandatory and represents contents of the comment.
    Field date is automatically set to the creatin date. Field forum_topic is
    used to connect comment to parent topic and field author is used to connect
    comment to its author. Both fields are mandatory. If one of the foreign key
    objects is deleted, comment is also deleted.
    """
    contents = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    forum_topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
