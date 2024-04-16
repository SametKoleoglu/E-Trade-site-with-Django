from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name='login'),
    path('profile/', views.profil, name='profile'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('products/', views.Products, name='products'),
    path('product_detail/<int:product_id>/', views.ProductDetail, name='product_detail'),
    path('basket/', views.Basket, name='basket'),
    path('favorite/', views.favorite, name='favorite'),
]
