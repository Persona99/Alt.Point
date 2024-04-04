from rest_framework import serializers
from .models import Client, Child, ChildClient


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class GetClientsResponse(serializers.ModelSerializer):

    children = serializers.SerializerMethodField('get_children')

    class Meta:
        model = Client
        fields = '__all__'
        depth = 1

    def get_children(self, instance):
        children = Child.objects.filter(child__client=instance)
        return ChildSerializer(children, many=True).data
