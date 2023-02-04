import logging

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stack_underflow_app.models import Comment, PostType
from stack_underflow_app.permissions import CustomPermissions

logger = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "body",
            "author",
            "post_id",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        author = self.context["author"]
        comment = Comment.objects.create(body=validated_data["body"],
                                         post_id=validated_data["post_id"],
                                         post_type=self.context["post_type"],
                                         author=author)
        return comment


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CustomPermissions]

    def create(self, request, post_type, post_pk):
        comment_data = request.data
        comment_data["post_id"] = post_pk
        author = request.user
        serializer = self.get_serializer(data=comment_data,
                                         context={
                                            "author": author,
                                            "post_type": post_type,
                                         })
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        logger.info(msg=f"Comment saved successfully with Id {comment.id}")
        return Response(status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        comment_data = request.data
        comment = self.get_object()
        if request.user != comment.author:
            # Only the author of the question should be able to update the Comment
            return Response(status=status.HTTP_403_FORBIDDEN)
        if ("author" in comment_data):
            return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Cannot modify 'author' or 'post_id' fields"}
                )
        serializer = self.get_serializer(comment, data=comment_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(msg=f"Comment with {comment.id} updated successfully")
        return Response(status=status.HTTP_200_OK)


class QuestionCommentViewSet(CommentViewSet):
    post_type = PostType.objects.get(name=PostType.QUES)
    queryset = Comment.objects.filter(post_type=post_type)

    def create(self, request, **kwargs):
        return super().create(request, post_type=self.post_type, post_pk=kwargs["question_pk"])


class AnswerCommentViewSet(CommentViewSet):
    post_type = PostType.objects.get(name=PostType.ANS)
    queryset = Comment.objects.filter(post_type=post_type)

    def create(self, request, **kwargs):
        return super().create(request, post_type=self.post_type, post_pk=kwargs["answer_pk"])
