import logging
from json import dumps, loads

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.models import Tag

logger = logging.getLogger(__name__)


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Tag
        fields = ['name', 'description']

    def create(self, validated_data):
        if not validated_data:
            return None
        data_dict = loads(dumps(validated_data))
        tag_name = data_dict.get('name')
        tag_desc = data_dict.get('description')
        tag = Tag(name=tag_name, description=tag_desc)
        tag, _ = Tag.objects.get_or_create(name=tag_name, defaults= {'description':tag_desc})
        return tag       


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
