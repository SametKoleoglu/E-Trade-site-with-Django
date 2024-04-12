from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name='login'),
    path('profile/', views.Profile, name='profile'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('categories/', views.Category, name='categories'),
]
