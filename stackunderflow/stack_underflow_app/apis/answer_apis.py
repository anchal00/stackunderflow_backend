import logging

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.models import Answer, PostType, Votes
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
        if data.get("is_accepted"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data["author"] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.save()
        logger.info(msg=f"Answer with id: {answer.id} posted successfully by: {request.user}")
        return Response(status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        answer = self.get_object()
        question = answer.question
        if request.user != question.author:
            # Only the author of the question should be able to update the Question
            return Response(status=status.HTTP_403_FORBIDDEN)
        if data.get("question") or data.get("author"):
            return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Cannot modify 'author' or 'question' fields"}
                )
        if data.get("is_accepted") and question.accepted_answer:
            return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Cannot accept multiple answers for a question"}
                )
        serializer = self.get_serializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(msg=f"Answer with Id {answer.id} updated successfully")
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def upvote(self, request, pk):
        user_id = request.user.id
        answer_id = pk
        vote, created = Votes.objects.get_or_create(post_id=answer_id,
                                                    post_type=PostType.objects.get(name=PostType.ANS),
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
        logger.info(msg=f"Vote with Id {vote.id} recorded successfully for Answer with Id {answer_id}")
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def downvote(self, request, pk):
        user_id = request.user.id
        answer_id = pk
        vote, created = Votes.objects.get_or_create(post_id=answer_id,
                                                    post_type=PostType.objects.get(name=PostType.ANS),
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
        logger.info(msg=f"Vote with Id {vote.id} recorded successfully for Answer with Id {answer_id}")
        return Response(status=status.HTTP_200_OK)
