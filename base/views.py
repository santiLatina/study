from django.shortcuts import render, redirect
from .models import Room
from .forms import  RoomForm
# Create your views here.

'''
rooms = [ 
    {'id': 1, 'name': 'Room1'},
    {'id': 2, 'name': 'Room2'},
    {'id': 3, 'name': 'Room3'}
]
'''   

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request,'base/home.html',context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/rooms.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)
