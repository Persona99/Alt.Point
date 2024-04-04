from django.contrib import admin
from django.urls import path, include
from .views import Clients

urlpatterns = [
    path('clients/', Clients.as_view())
]
