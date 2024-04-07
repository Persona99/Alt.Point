from rest_framework import serializers
from .models import Client, Child, Document, Job, Communication, Passport, Address


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class ComunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = '__all__'


class PasportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'


class AddressSserializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class GetClientsResponse(serializers.ModelSerializer):
    children = ChildSerializer(many=True)
    documentIds = DocumentSerializer(many=True)
    jobs = DocumentSerializer(many=True)
    communications = ComunicationSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'surname', 'patronymic', 'dob', 'children', 'documentIds',
                  'passport', 'livingAddress', 'regAddress', 'jobs', 'typeEducation', 'monIncome',
                  'monExpenses', 'communications', 'createAt', 'updateAt']
        depth = 1


class SpouseSerializer(serializers.ModelSerializer):
    id = None
    children = ChildSerializer(many=True)
    documentIds = DocumentSerializer(many=True)
    jobs = DocumentSerializer(many=True)
    communications = ComunicationSerializer(many=True)
    passport = PasportSerializer(required=False)
    livingAddress = AddressSserializer(required=False)
    regAddress = AddressSserializer(required=False)

    class Meta:
        model = Client
        fields = '__all__'


class PostClientRequest(serializers.ModelSerializer):
    id = None
    children = ChildSerializer(many=True)
    documentIds = DocumentSerializer(many=True)
    jobs = DocumentSerializer(many=True)
    communications = ComunicationSerializer(many=True)
    passport = PasportSerializer(required=False)
    livingAddress = AddressSserializer(required=False)
    regAddress = AddressSserializer(required=False)
    spouse = SpouseSerializer(required=False)

    class Meta:
        model = Client
        fields = '__all__'

    def _get_data(self, validated_data) -> dict:
        children = validated_data.pop('children')
        documents = validated_data.pop('documentIds')
        jobs = validated_data.pop('jobs')
        communications = validated_data.pop('communications')
        passport = validated_data.pop('passport')
        livingAddress = validated_data.pop('livingAddress')
        regAddress = validated_data.pop('regAddress')
        return {'many_to_many': {'children': children, 'documents': documents, 'jobs': jobs,
                'communications': communications, }, 'passport': passport, 'livingAddress': livingAddress,
                'regAddress': regAddress, 'validated_data': validated_data}

    def _add_many_to_many_rel_fields(self, client: Client, data: dict) -> Client:
        print(data)
        if data['children']:
            client.children.add(Child(**child) for child in data['children'])
        if data['documents']:
            client.documentIds.add(Child(**document)
                                   for document in data['documents'])
        if data['jobs']:
            client.jobs.add(Child(**job) for job in data['jobs'])
        if data['communications']:
            client.communications.add(Child(**communication)
                                      for communication in data['communications'])
        return client

    def _create_client(self, validated_data) -> Client:
        data: dict = self._get_data(validated_data)
        livingAddress = Address.objects.create(**data['livingAddress'])
        regAddress = Address.objects.create(**data['regAddress'])
        passport = Passport.objects.create(**data['passport'])
        client = Client.objects.create(passport=passport, livingAddress=livingAddress,
                                       regAddress=regAddress, **data['validated_data'])
        client = self._add_many_to_many_rel_fields(
            client, data['many_to_many'])
        return client

    def create(self, validated_data) -> Client:
        spouse = validated_data.pop('spouse')
        client: Client = self._create_client(validated_data)
        spouse = self._create_client(spouse)
        client.spouse = spouse
        client.save()
        return client
