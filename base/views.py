from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def Home(request):
    return HttpResponse("Home")


def Room(request):
    return HttpResponse("Room")