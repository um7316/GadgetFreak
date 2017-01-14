from django.test import TestCase

from django.contrib.auth.models import User
from django.core.files import File

import StringIO
from PIL import Image

from .models import Device, ForumTopic, Comment

# Create your tests here.
class ForumTopicTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='test_user')

    def test_forum_topic_comments_no(self):
        test_img = Image.new(mode="RGBA", size=(20, 20), color=(0, 0, 0, 0))
        image_file = StringIO.StringIO()
        test_img.save(image_file, 'JPEG', quality=90)
        f = File(image_file)

        d = Device(title="Test device", description="test", img_1=f, author=self.u1)
        d.save()

        ft = ForumTopic(device=d, name="c1", topic_type="C", contents="contents", author=self.u1)
        ft.save()

        c1 = Comment(contents="test comment", forum_topic=ft, author=self.u1)
        c1.save()

        self.assertEqual(ft.get_no_comments(), 1)

        c1 = Comment(contents="test comment", forum_topic=ft, author=self.u1)
        c1.save()

        self.assertEqual(ft.get_no_comments(), 2)

    def tearDown(self):
        self.u1.delete()
