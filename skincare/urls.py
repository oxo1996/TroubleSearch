from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.skincare, name="skin"),
    path('toner/', views.toner, name="toner"),
    path('essence/', views.essence, name="essence"),
    path('lotion/', views.lotion, name="lotion"),
    path('cream/', views.cream, name="cream"),
    path('searchSkincare/', views.changeItem, name="searchSkincare"),
]