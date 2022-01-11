from django.urls import path
from . import views

urlpatterns = [
    #Login paths
    path('login/', views.loginPage, name="Login"),
    path('logout/', views.logoutPage, name="Logout"),
    path('register/', views.registerPage, name="Register"),
    
    #Home path
    path('', views.home, name="Home"),

    #Rooms path
    path('room/<str:pk>/', views.room, name="Room"),
    path('create_room/', views.createRoom, name="create-room"),
    path('update_room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete-room"),
    

    #Message Path
    path('delete_message/<str:pk>/', views.deleteMessage, name="delete-message"),

    #Profile path
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update_user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="Topics"),
    path('activity/', views.activitiesPage, name="Activity"),
]