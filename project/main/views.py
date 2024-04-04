from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from .serializers import GetClientsResponse
from .models import Client
# Create your views here.


class Clients(APIView):
    def get(self, request: Request) -> Response:
        instances = Client.objects.all()
        serializer = GetClientsResponse(instances, many=True)
        data = {
            'limit': 10,
            'page': 1,
            'total': 1,
            'data': serializer.data
        }
        return Response(data=data, status=200)
