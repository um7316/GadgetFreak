from django.test import TestCase

from django.contrib.auth.models import User
from django.core.files import File

import StringIO
from PIL import Image

from .models import Device, ForumTopic

# Create your tests here.
class DeviceTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='test_user')

    def test_device_comments_no(self):
        test_img = Image.new(mode="RGBA", size=(20, 20), color=(0, 0, 0, 0))
        image_file = StringIO.StringIO()
        test_img.save(image_file, 'JPEG', quality=90)
        f = File(image_file)

        d = Device(title="Test device", description="test", img_1=f, author=self.u1)
        d.save()

        r1 = ForumTopic(device=d, name="r1", topic_type="C", contents="contents", author=self.u1)
        r1.save()

        self.assertEqual(d.get_no_comments(), 1)

        r2 = ForumTopic(device=d, name="r2", topic_type="C", contents="contents", author=self.u1)
        r2.save()

        self.assertEqual(d.get_no_comments(), 2)

    def test_device_reviews_no(self):
        test_img = Image.new(mode="RGBA", size=(20, 20), color=(0, 0, 0, 0))
        image_file = StringIO.StringIO()
        test_img.save(image_file, 'JPEG', quality=90)
        f = File(image_file)

        d = Device(title="Test device", description="test", img_1=f, author=self.u1)
        d.save()

        r1 = ForumTopic(device=d, name="r1", topic_type="R", contents="contents", score="2.5", author=self.u1)
        r1.save()

        self.assertEqual(d.get_no_reviews(), 1)

        r2 = ForumTopic(device=d, name="r2", topic_type="R", contents="contents", score="3.5", author=self.u1)
        r2.save()

        self.assertEqual(d.get_no_reviews(), 2)

    def test_device_score(self):
        test_img = Image.new(mode="RGBA", size=(20, 20), color=(0, 0, 0, 0))
        image_file = StringIO.StringIO()
        test_img.save(image_file, 'JPEG', quality=90)
        f = File(image_file)

        d = Device(title="Test device", description="test", img_1=f, author=self.u1)
        d.save()

        r1 = ForumTopic(device=d, name="r1", topic_type="R", contents="contents", score="2.5", author=self.u1)
        r1.save()

        self.assertEqual(d.get_score(), 2.5)

        r2 = ForumTopic(device=d, name="r2", topic_type="R", contents="contents", score="3.5", author=self.u1)
        r2.save()

        self.assertAlmostEqual(d.get_score(), 3)

    def tearDown(self):
        self.u1.delete()
