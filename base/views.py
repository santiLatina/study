from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Room, Topic
from .forms import  RoomForm
from django.contrib.auth.forms import UserCreationForm
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
            """ Create the session """
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
    '''Room obtains a queryset of any of topic,name or description'''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request,'base/home.html',context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body') #Esto lo recibo del template de room
        )
        '''Agrego como participante un usuario si habla en la sala'''
        room.participants.add(request.user)
        return redirect('Room',pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html',context)


@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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


@login_required(login_url='Login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this.')

    if request.method == 'POST':
        message.delete()
        return redirect('Home')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

