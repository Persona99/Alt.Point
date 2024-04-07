from rest_framework.views import APIView, Response, Request
from .serializers import GetClientsResponse, PostClientRequest, PatchClientSerializer
from .models import Client
from datetime import datetime
from django.db.models import F, Q
# Create your views here.


class Clients(APIView):
    def get(self, request: Request) -> Response:
        #     try:
        limit = int(request.query_params.get('limit', 10))
        page = int(request.query_params.get('page', 1))
        sortBy = request.query_params.get('sortBy', 'createAt')
        sortDir = request.query_params.get('sortDir', 'asc')
        search = request.query_params.get('search', '')
        if sortDir == 'desc':
            instances = Client.objects.all().filter(deleteAt=None).filter(
                Q(name__contains=search) | Q(surname__contains=search) | Q(patronymic__contains=search)).order_by(
                    F(sortBy).desc())[(page-1)*limit:page*limit]
        else:
            instances = Client.objects.all().filter(deleteAt=None).filter(
                Q(name__contains=search) | Q(surname__contains=search) | Q(patronymic__contains=search)).order_by(
                    F(sortBy).asc())[(page-1)*limit:page*limit]
        serializer = GetClientsResponse(instances, many=True)
        data = {
            'limit': limit,
            'page': page,
            'total': Client.objects.filter(deleteAt=None).count(),
            'data': serializer.data
        }
        return Response(data=data, status=200)
        # except:
        #     return Response(data={"status": 500, "code": "INTERNAL_SERVER_ERROR"}, status=500)

    def post(self, request: Request) -> Response:
        try:
            client = PostClientRequest(data=request.data)
            if not client.is_valid():
                return Response(data=client.errors, status=422)
            client.save()
            return Response(data={client.data['id']}, status=201)
        except:
            return Response(data={"status": 500, "code": "INTERNAL_SERVER_ERROR"}, status=500)


class OneClient(APIView):
    def get(self, request: Request) -> Response:
        try:
            id = request.query_params.get('clientId')
            client = Client.objects.filter(id=id, deleteAt=None).first()
            if not client:
                return Response(data={'status': 404, 'code': 'ENTITY_NOT_FOUND'}, status=404)
            client = GetClientsResponse(client)
            return Response(data=client.data)
        except:
            return Response(data={"status": 500, "code": "INTERNAL_SERVER_ERROR"}, status=500)

    def patch(self, request: Request) -> Response:
        try:
            id = request.query_params.get('clientId')
            client = Client.objects.filter(id=id, deleteAt=None).first()
            if not client:
                return Response(data={'status': 404, 'code': 'ENTITY_NOT_FOUND'}, status=404)
            client_serializer = PatchClientSerializer(
                data=request.data, instance=client)
            client_serializer.is_valid(raise_exception=True)
            client_serializer.save()
            return Response(status=204)
        except:
            return Response(data={"status": 500, "code": "INTERNAL_SERVER_ERROR"}, status=500)

    def delete(self, request: Request) -> Response:
        try:
            id = request.query_params.get('clientId')
            client = Client.objects.filter(id=id, deleteAt=None).first()
            if not client:
                return Response(data={'status': 404, 'code': 'ENTITY_NOT_FOUND'}, status=404)
            client.deleteAt = datetime.now()
            client.save()
            return Response(data={client.id}, status=201)
        except:
            return Response(data={"status": 500, "code": "INTERNAL_SERVER_ERROR"}, status=500)
