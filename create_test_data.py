from gadgetfreak_web.models import Device, ForumTopic
from django.core.files import File

import StringIO
from PIL import Image

import random

test_img = Image.new(mode="RGBA", size=(20, 20), color=(0, 0, 0, 0))
image_file = StringIO.StringIO()
test_img.save(image_file, 'JPEG', quality=90)
f = File(image_file)

for i in range(50):
    d = Device(title="A test {}".format(i), description="test", img_1=f, author_id=1)
    d.save()
    for j in range(20):
        r = ForumTopic(device=d, name="r {}".format(j), topic_type="R", contents="contents", score=str(random.randrange(10, 50) / 10.0), author_id=1)
        r.save()


# komentar
