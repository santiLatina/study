from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="Login"),
    path('logout/', views.logoutUser, name="Logout"),
    path('', views.home, name="Home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('create_room/', views.createRoom, name="create-room"),
    path('update_room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete-room"),

]