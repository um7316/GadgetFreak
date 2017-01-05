from django.shortcuts import render

from .models import Device

# Create your views here.

def index(request):
    slovar_preslikav = dict()
    slovar_preslikav["devices"] = Device.objects.all()
    return render(request, "landing.html", slovar_preslikav)
