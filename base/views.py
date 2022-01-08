from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import  RoomForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from base import forms
# Create your views here.

'''
rooms = [ 
    {'id': 1, 'name': 'Room1'},
    {'id': 2, 'name': 'Room2'},
    {'id': 3, 'name': 'Room3'}
]
'''   

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            """ Create de session """
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, 'Username or Password does not exist.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('Home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, 'An error occurred during registration.')

    context = {'form' : form}
    return render(request, 'base/login_register.html',context) 


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count}
    return render(request,'base/home.html',context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/rooms.html',context)


@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='Login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) #El formulario de solo la habitacion instanciada aqui
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='Login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

