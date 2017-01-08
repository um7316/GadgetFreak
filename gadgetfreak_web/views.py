from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Device, TechnicalSpecification
from .forms import LoginForm

# Create your views here.

def index(request):
    slovar_preslikav = dict()
    slovar_preslikav["devices"] = Device.objects.all()
    return render(request, "landing.html", slovar_preslikav)

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

    sp = {"device": device}

    return render(request, "add-device.html", sp)
