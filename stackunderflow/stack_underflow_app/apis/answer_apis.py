import logging

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.apis.comment_apis import CommentSerializer
from stack_underflow_app.models import Answer, Comment, PostType, Votes
from stack_underflow_app.permissions import (CustomPermissions,
                                             HasEnoughReputationPoints)

logger = logging.getLogger(__name__)


class AnswerSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    upvotes = serializers.ReadOnlyField()
    downvotes = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data, **kwargs):
        request = kwargs.pop("request")
        if "question" in validated_data or "author" in validated_data:
            raise serializers.ValidationError(detail={"error": "Cannot modify given fields"})
        if (
            ("is_accepted" in validated_data and request.user != instance.question.author)
            or instance.question.accepted_answer
        ):
            raise serializers.ValidationError(detail={"error": "Cannot update given fields"})
        if "answer_body" in validated_data:
            instance.answer_body = validated_data["answer_body"]
            instance.save(update_fields=["answer_body"])
            return instance
        return serializers.ValidationError(detail={"error": "Request payload empty"})

    def get_comments(self, obj):
        comments = Comment.objects.filter(post_type=PostType.objects.get(name=PostType.ANS),
                                          post_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [CustomPermissions]

    def create(self, request, **kwargs):
        data = request.data
        user = request.user.id
        if not bool(data and data.get("answer_body")):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if data.get("is_accepted"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data["author"] = user
        data["question"] = kwargs["question_pk"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.save()
        logger.info(msg=f"Answer with id: {answer.id} posted successfully by: {request.user}")
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        question_pk = kwargs["question_pk"]
        return Response(status=status.HTTP_200_OK,
                        data=self.get_serializer(self.queryset.filter(question_id=question_pk), many=True).data)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        answer = self.get_object()
        if request.user != answer.author:
            # Only the author of the answer should be able to update the Answer
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(answer, data=request.data, context={"request": request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(answer, data)
        logger.info(msg=f"Answer with Id {answer.id} updated successfully")
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, permission_classes=[HasEnoughReputationPoints])
    def upvote(self, request, **kwargs):
        user_id = request.user.id
        answer_id = kwargs["pk"]
        if self.get_object().author == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        vote, created = Votes.objects.get_or_create(post_id=answer_id,
                                                    post_type=PostType.objects.get(name=PostType.ANS),
                                                    user_id=user_id,
                                                    defaults={"upvote": True, "downvote": False})
        had_already_voted = not created
        vote_id = vote.id
        if had_already_voted:
            if vote.upvote:
                # Remove the vote if user had already upvoted and now upvotes again
                vote.delete()
            else:
                # Previous vote was a downvote and now user is upvoting
                vote.upvote = True
                vote.downvote = False
                vote.save()
        logger.info(msg=f"Vote with Id {vote_id} recorded successfully for Answer with Id {answer_id}")
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, permission_classes=[HasEnoughReputationPoints])
    def downvote(self, request, **kwargs):
        user_id = request.user.id
        answer_id = kwargs["pk"]
        if self.get_object().author == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        vote, created = Votes.objects.get_or_create(post_id=answer_id,
                                                    post_type=PostType.objects.get(name=PostType.ANS),
                                                    user_id=user_id,
                                                    defaults={"upvote": False, "downvote": True})
        had_already_voted = not created
        vote_id = vote.id
        if had_already_voted:
            if vote.downvote:
                # Remove the vote if user had already downvoted and now downvotes again
                vote.delete()
            else:
                # Previous vote was a upvote and now user is downvoting
                vote.upvote = False
                vote.downvote = True
                vote.save()
        logger.info(msg=f"Vote with Id {vote_id} recorded successfully for Answer with Id {answer_id}")
        return Response(status=status.HTTP_200_OK)
