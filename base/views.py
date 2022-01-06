from django.shortcuts import render

# Create your views here.

rooms = [ 
    {'id': 1, 'name': 'Room1'},
    {'id': 2, 'name': 'Room2'},
    {'id': 3, 'name': 'Room3'}
]
    

def Home(request):
    context = {'rooms': rooms}
    return render(request,'base/home.html',context)


def Room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/rooms.html',context)