import logging
from json import dumps, loads

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.apis.tag_apis import TagSerializer
from stack_underflow_app.models import Question, Tag
from stack_underflow_app.permissions import QuestionAPIPermissions

logger = logging.getLogger(__name__)


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=False)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    upvotes = serializers.ReadOnlyField()
    downvotes = serializers.ReadOnlyField()
    viewcount = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    author = serializers.StringRelatedField(read_only=True)
    closing_remark = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        logger.info(msg='Creating Question object')
        # Serializing the validated data and then De-Serializing it again,
        # to convert OrderedDict into Dict for easier use
        tags_data = loads(dumps(validated_data.pop('tags')))
        # User who posted the question
        user = self.context['request'].user
        serializer = TagSerializer(data=tags_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        tag_objects = []
        for tag in tags_data:
            tag_objects.append(Tag.objects.get(name=tag['name']))
        question = Question.objects.create(**validated_data)
        question.author = user
        question.save()
        question.tags.set(tag_objects)
        return question


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [QuestionAPIPermissions]

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return QuestionSerializer(self.queryset, many=True)
        question_data = kwargs["data"]
        return QuestionSerializer(data=question_data, context={'request': kwargs["request"]})

    def list(self, request):
        serializer = self.get_serializer()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        question_data = request.data
        question_serializer = self.get_serializer(data=question_data, request=request)
        question_serializer.is_valid(raise_exception=True)
        question = question_serializer.save()
        logger.info(msg=f'Question with id: {question.id} posted successfully by: {request.user}')
        return Response(status=status.HTTP_201_CREATED)
