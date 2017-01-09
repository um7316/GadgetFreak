from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Device, TechnicalSpecification, ForumTopic, Comment
from .forms import LoginForm, DeviceForm, TechnicalSpecificationForm, ForumTopicForm, CommentForm

# Create your views here.

def index(request):
    sp = {
        "devices": Device.objects.all(),
        "reviews": ForumTopic.objects.filter(topic_type="R").order_by("-date")[:5]
    }
    return render(request, "landing.html", sp)

def login_view(request):
    if request.method == "POST" and request.POST["return_url"]:
        # request.POST -> slovar vsebine
        lf = LoginForm(request.POST)
        if lf.is_valid():
            u = authenticate(username=lf.cleaned_data["username"], password=lf.cleaned_data["password"])
            if u is not None:
                login(request, u) # poveze sejo z uporabnikom
        return HttpResponseRedirect(request.POST["return_url"])
    else:
        raise Http404

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def device_info(request, device_id):
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    sp = {"device": device}

    sub_images = {i: e for i, e in enumerate([device.img_1, device.img_2, device.img_3, device.img_4], start=1) if e}
    img_no = request.GET.get("img", "1")
    if img_no == "2" and device.img_2:
        sp["main_img"] = device.img_2
        del sub_images[2]
    elif img_no == "3" and device.img_3:
        sp["main_img"] = device.img_3
        del sub_images[3]
    elif img_no == "4" and device.img_4:
        sp["main_img"] = device.img_4
        del sub_images[4]
    else:
        sp["main_img"] = device.img_1
        del sub_images[1]

    sp["sub_images"] = sub_images

    sp["specs"] = TechnicalSpecification.objects.filter(device_id=device.id)
    return render(request, "device-info.html", sp)


def device_edit(request, device_id):
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    if request.method == "POST":
        device_form = DeviceForm(request.POST, request.FILES, instance=device)

        # check technical specs
        ts = []
        correct = 0
        for i in range(100):
            if str(i)+"-name" not in request.POST:
                break
            ts_form = TechnicalSpecificationForm(request.POST, prefix=str(i))
            if ts_form.is_valid():
                correct += 1
            ts.append(ts_form)

        if correct == len(ts) and device_form.is_valid():
            # vsi podatki so pravilni, lahko shranimo
            d = device_form.save()

            TechnicalSpecification.objects.filter(device_id=device.id).delete()
            for tsf in ts:
                ts_instance = tsf.save(commit=False)
                if ts_instance.name and ts_instance.value:
                    ts_instance.device_id = device.id
                    ts_instance.save()

            return HttpResponseRedirect(reverse("device_info", kwargs={"device_id": d.id}))

    else:
        device_form = DeviceForm(instance=device)

        ts = [TechnicalSpecificationForm(instance=ts, prefix=str(i)) for i, ts in enumerate(TechnicalSpecification.objects.filter(device_id=device.id))]
        fields = int(request.GET.get("fields", "0")) or len(ts) + 2
        if fields < len(ts) or fields > 100:
            return HttpResponseBadRequest()
        ts += [TechnicalSpecificationForm(prefix=str(i)) for i in range(len(ts), fields)]

    sp = {"device": device, "device_form": device_form, "specs": ts}

    return render(request, "add-device.html", sp)

def device_add(request):
    if request.method == "POST":
        device_form = DeviceForm(request.POST, request.FILES)

        # check technical specs
        ts = []
        correct = 0
        for i in range(100):
            if str(i)+"-name" not in request.POST:
                break
            ts_form = TechnicalSpecificationForm(request.POST, prefix=str(i))
            if ts_form.is_valid():
                correct += 1
            ts.append(ts_form)

        if correct == len(ts) and device_form.is_valid():
            # vsi podatki so pravilni, lahko shranimo
            d = device_form.save()

            for tsf in ts:
                ts_instance = tsf.save(commit=False)
                if ts_instance.name and ts_instance.value:
                    ts_instance.device_id = d.id
                    ts_instance.save()

            return HttpResponseRedirect(reverse("device_info", kwargs={"device_id": d.id}))

    else:
        device_form = DeviceForm()
        fields = int(request.GET.get("fields", "4"))
        if fields > 100:
            return HttpResponseBadRequest()
        ts = [TechnicalSpecificationForm(prefix=str(i)) for i in range(fields)]

    sp = {"device": None, "device_form": DeviceForm(), "specs": ts}

    return render(request, "add-device.html", sp)

def device_forum(request, device_id):
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    topics = ForumTopic.objects.filter(device_id=device.id)
    for topic in topics:
        topic.comments_no = Comment.objects.filter(forum_topic_id=topic.id).count()

    sp = {"device": device, "topics": topics}

    return render(request, "device-forum.html", sp)

def add_topic(request, device_id):
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    if request.method == "POST":
        topic_form = ForumTopicForm(request.POST, request.FILES)
        if topic_form.is_valid():
            ft_instance = topic_form.save(commit=False)
            if ft_instance.topic_type == ft_instance.COMMENT_TYPE or \
                    ft_instance.image and ft_instance.score:
                ft_instance.device_id = device.id
                ft_instance.author_id = request.user.id
                ft_instance.save()
                return HttpResponseRedirect(reverse("device_forum", kwargs={"device_id": device.id}))
            else:
                print(ft_instance.image, ft_instance.score)
    else:
        topic_form = ForumTopicForm()

    sp = {"device": device, "topic_form": topic_form}

    return render(request, "add-topic.html", sp)

def topic(request, device_id, topic_id):
    device = Device.objects.filter(id=device_id).first()
    topic = ForumTopic.objects.filter(id=topic_id).first()
    if not device or not topic:
        raise Http404

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cf_instance = comment_form.save(commit=False)
            cf_instance.forum_topic_id = topic.id
            cf_instance.author_id = request.user.id
            cf_instance.save()
            return HttpResponseRedirect(reverse("topic", kwargs={"device_id": device.id, "topic_id": topic.id}))
    else:
        comment_form = CommentForm()

    sp = {
        "device": device,
        "topic": topic,
        "comments": Comment.objects.filter(forum_topic_id=topic.id),
        "comment_form": comment_form
    }

    return render(request, "topic.html", sp)
