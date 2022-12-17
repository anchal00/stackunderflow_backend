import logging
from json import dumps, loads

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.apis.answer_apis import AnswerSerializer
from stack_underflow_app.apis.comment_apis import CommentSerializer
from stack_underflow_app.apis.tag_apis import TagSerializer
from stack_underflow_app.models import (Answer, Comment, PostType, Question,
                                        Tag, Votes)
from stack_underflow_app.permissions import CustomPermissions

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
    answers = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        logger.info(msg="Creating Question object")
        # Serializing the validated data and then De-Serializing it again,
        # to convert OrderedDict into Dict for easier use
        tags_data = loads(dumps(validated_data.pop("tags")))
        # User who posted the question
        user = self.context["request"].user
        serializer = TagSerializer(data=tags_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        tag_objects = []
        for tag in tags_data:
            tag_objects.append(Tag.objects.get(name=tag["name"]))
        question = Question.objects.create(**validated_data)
        question.author = user
        question.save()
        question.tags.set(tag_objects)
        return question

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = Comment.objects.filter(post_type=PostType.objects.get(name=PostType.QUES),
                                          post_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomPermissions]

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return QuestionSerializer(self.queryset, many=True)
        elif self.action == "retrieve":
            return QuestionSerializer(kwargs["data"])
        return QuestionSerializer(data=kwargs["data"], context={"request": kwargs["request"]})

    def list(self, request):
        serializer = self.get_serializer()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        question_data = request.data
        question_serializer = self.get_serializer(data=question_data, request=request)
        question_serializer.is_valid(raise_exception=True)
        question = question_serializer.save()
        logger.info(msg=f"Question with id: {question.id} posted successfully by: {request.user}")
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        serializer = self.get_serializer(data=self.get_object())
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["POST"], detail=True)
    def upvote(self, request, pk):
        user_id = request.user.id
        question_id = pk
        vote, created = Votes.objects.get_or_create(post_id=question_id,
                                                    post_type=PostType.objects.get(name=PostType.QUES),
                                                    user_id=user_id,
                                                    defaults={"upvote": True, "downvote": False})
        had_already_voted = not created
        if had_already_voted:
            if vote.upvote:
                # Remove the vote if user had already upvoted and now upvotes again
                vote.delete()
            else:
                # Previous vote was a downvote and now user is upvoting
                vote.upvote = True
                vote.downvote = False
                vote.save()
        logger.info(msg=f"Vote with Id {vote.id} recorded successfully")
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def downvote(self, request, pk):
        user_id = request.user.id
        question_id = pk
        vote, created = Votes.objects.get_or_create(post_id=question_id,
                                                    post_type=PostType.objects.get(name=PostType.QUES),
                                                    user_id=user_id,
                                                    defaults={"upvote": False, "downvote": True})
        had_already_voted = not created
        if had_already_voted:
            if vote.downvote:
                # Remove the vote if user had already downvoted and now downvotes again
                vote.delete()
            else:
                # Previous vote was a upvote and now user is downvoting
                vote.upvote = False
                vote.downvote = True
                vote.save()
        logger.info(msg=f"Vote with Id {vote.id} recorded successfully")
        return Response(status=status.HTTP_200_OK)
