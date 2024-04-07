from rest_framework.views import APIView, Response, Request
from .serializers import GetClientsResponse, PostClientRequest
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

    def post(self, request: Request) -> Response:
        client = PostClientRequest(data=request.data)
        if not client.is_valid():
            return Response(data=client.errors, status=422)
        client.save()
        return Response(data={client.data['id']}, status=201)


class OneClient(APIView):
    def get(self, request: Request) -> Response:
        id = request.query_params.get('clientId')

        client = Client.objects.filter(id=id).first()
        if not client:
            return Response(data={'status': 404, 'code': 'ENTITY_NOT_FOUND'}, status=404)
        client = GetClientsResponse(client)
        return Response(data=client.data)
