from rest_framework import serializers
from .models import Client, Child, Document, Job, Communication, Passport, Address
from .models import EducationType


class ChildSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Child
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Document
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Job
        fields = '__all__'


class ComunicationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Communication
        fields = '__all__'


class PasportSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Passport
        fields = '__all__'


class AddressSserializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

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
        exclude = ['spouse']
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


class PatchClientSerializer(serializers.ModelSerializer):
    id = None
    children = ChildSerializer(many=True, required=False)
    documentIds = DocumentSerializer(many=True, required=False)
    jobs = DocumentSerializer(many=True, required=False)
    communications = ComunicationSerializer(
        many=True, required=False, allow_null=True)
    passport = PasportSerializer(required=False, allow_null=True)
    livingAddress = AddressSserializer(required=False, allow_null=True)
    regAddress = AddressSserializer(required=False, allow_null=True)
    spouse = SpouseSerializer(required=False)
    dob = serializers.DateTimeField(required=False)
    typeEducation = serializers.ChoiceField(
        choices=EducationType, required=False)

    class Meta:
        model = Client
        fields = '__all__'

    def _update_passport(self, instance: Client, passport: dict) -> None:
        if not passport:
            if not instance.passport:
                return
            instance.passport.delete()
        else:
            if passport.get('id'):
                Passport.objects.filter(
                    id=passport.get('id')).update(**passport)
            else:
                instance.passport = Passport.objects.create(**passport)

    def _update_children(self, instance: Client, children: list) -> None:
        if not children:
            if not instance.children:
                return
            instance.children.delete()
        for child in children:
            if child.get(id):
                child_instance = Child.objects.filter(id=child.get(id))
                if not child_instance:
                    continue
                child_instance.update(**child)
            else:
                instance.children.add(Child.objects.create(**child))

    def _update_documentIds(self, instance: Client, documentIds: list) -> None:
        if not documentIds:
            if not instance.documentIds:
                return
            instance.documentIds.delete()
        for document in documentIds:
            if document.get(id):
                doc_instance = Document.objects.filter(id=document.get(id))
                if not doc_instance:
                    continue
                doc_instance.update(**document)
            else:
                instance.children.add(Child.objects.create(**document))

    def _update_livingAddress(self, instance: Client, livingAddress: dict) -> None:
        if not livingAddress:
            if not instance.livingAddress:
                return
            instance.livingAddress.delete()
        else:
            if livingAddress.get('id'):
                Address.objects.filter(id=livingAddress.get(
                    'id')).update(**livingAddress)
            else:
                instance.livingAddress = Address.objects.create(
                    **livingAddress)

    def _update_regAddress(self, instance: Client, regAddress: dict) -> None:
        if not regAddress:
            if not instance.regAddress:
                return
            instance.regAddress.delete()
        else:
            if regAddress.get('id'):
                Address.objects.filter(
                    id=regAddress.get('id')).update(**regAddress)
            else:
                instance.regAddress = Address.objects.create(**regAddress)

    def _update_jobs(self, instance: Client, jobs: list) -> None:
        if not jobs:
            if not instance.jobs:
                return
            instance.jobs.delete()
        for job in jobs:
            if job.get(id):
                job_instance = Job.objects.filter(id=job.get(id))
                if not job_instance:
                    continue
                job_instance.update(**job)
            else:
                instance.children.add(Child.objects.create(**job))

    def _update_communications(self, instance: Client, communications: list):
        if not communications:
            if not instance.communications:
                return
            instance.communications.delete()
        for com in communications:
            if com.get(id):
                com_instance = Communication.objects.filter(id=com.get(id))
                if not com_instance:
                    continue
                com_instance.update(**com)
            else:
                instance.children.add(Child.objects.create(**com))

    def _update_spouse(self, instance: Client, spouse: dict) -> None:
        if not spouse:
            if not instance.spouse:
                return
            instance.spouse.delete()
        else:
            if spouse.get('id'):
                Client.objects.get(id=spouse.get('id')).update(**spouse)
            else:
                instance.spouse = Client.objects.create(**spouse)

    def update(self, instance: Client, validated_data: dict) -> Client:
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get(
            'patronymic', instance.patronymic)
        instance.dob = validated_data.get('dob', instance.dob)
        passport = 'passport' in validated_data
        if passport:
            self._update_passport(instance, validated_data.get('passport'))
        children = validated_data.get('children', None)
        if children:
            self._update_children(instance, children)
        documentIds = validated_data.get('documentIds', None)
        if documentIds:
            self._update_documentIds(instance, documentIds)
        livingAddress = 'livingAddress' in validated_data
        if livingAddress:
            self._update_livingAddress(
                instance, validated_data.get('livingAddress'))
        regAddress = 'regAddress' in validated_data
        if regAddress:
            self._update_regAddress(instance, validated_data.get('regAddress'))
        jobs = validated_data.get('jobs', None)
        if jobs:
            self._update_jobs(instance, jobs)
        instance.typeEducation = validated_data.get(
            'typeEducation', instance.typeEducation)
        instance.monIncome = validated_data.get(
            'monIncome', instance.monIncome)
        instance.monExpenses = validated_data.get(
            'monExpenses', instance.monExpenses)
        communications = validated_data.get('communications', None)
        if communications:
            self._update_communications(instance, communications)
        spouse = validated_data.get('spouse', None)
        if spouse:
            self._update_spouse(instance, spouse)
        instance.save()
        return instance
