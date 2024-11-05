from rest_framework import serializers
from workspace.models import Studio, StudioStorage


class StudioFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudioStorage
        fields = '__all__'


class StudioSerializer(serializers.ModelSerializer):

    studio_files = StudioFileSerializer(many=True, read_only=True)

    class Meta:
        model = Studio
        fields = '__all__'
