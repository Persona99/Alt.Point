from django.urls import path
from .views import Clients, OneClient

urlpatterns = [
    path('clients/', Clients.as_view()),
    path('client/', OneClient.as_view())
]
