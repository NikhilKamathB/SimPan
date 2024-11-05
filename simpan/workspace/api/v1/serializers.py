from workspace.serializers import StudioSerializer


class StudioSerializerV1(StudioSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)