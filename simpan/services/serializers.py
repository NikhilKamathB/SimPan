from rest_framework import serializers
from django.contrib.auth.models import User
from db.models import Workspace, WorkspaceStorage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]


class WorkspaceFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkspaceStorage
        fields = '__all__'


class WorkspaceSerializer(serializers.ModelSerializer):

    workspace_files = WorkspaceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
