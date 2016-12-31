from django.shortcuts import render

# Create your views here.

def index(request):
    slovar_preslikav = dict()
    return render(request, "index.html", slovar_preslikav)
