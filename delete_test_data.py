from gadgetfreak_web.models import Device

print(Device.objects.filter(title__startswith="A test").count())
Device.objects.filter(title__startswith="A test").delete()
