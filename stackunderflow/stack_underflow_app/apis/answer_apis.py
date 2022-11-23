import logging

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.models import Answer
from stack_underflow_app.permissions import CustomPermissions

logger = logging.getLogger(__name__)


class AnswerSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    upvotes = serializers.ReadOnlyField()
    downvotes = serializers.ReadOnlyField()

    class Meta:
        model = Answer
        fields = "__all__"


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [CustomPermissions]

    def create(self, request):
        data = request.data
        user = request.user.id
        if not bool(
            data
            and data.get("question")
            and data.get("answer_body")
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data["author"] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
