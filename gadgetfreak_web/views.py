from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Device
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
    print(device_id)
    return render(request, "device-info.html", dict())
