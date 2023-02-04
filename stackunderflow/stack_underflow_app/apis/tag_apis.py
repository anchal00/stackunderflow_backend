import logging
from json import dumps, loads

from rest_framework import serializers, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.models import Tag

logger = logging.getLogger(__name__)


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        if not validated_data:
            return None
        data_dict = loads(dumps(validated_data))
        tag_name = data_dict.get("name")
        tag = Tag(name=tag_name)
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        return tag


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        tag_data = request.data
        serializer = self.get_serializer(data=tag_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(msg="Tag created successfully")
        return Response(status=status.HTTP_201_CREATED)
