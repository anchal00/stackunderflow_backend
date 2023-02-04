# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from stack_underflow_app.apis.answer_apis import AnswerViewSet
from stack_underflow_app.apis.comment_apis import (AnswerCommentViewSet,
                                                   QuestionCommentViewSet)
from stack_underflow_app.apis.question_apis import QuestionViewSet
from stack_underflow_app.apis.tag_apis import TagViewSet

router = routers.DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
router.register("answers", AnswerViewSet, basename="answers")
router.register("tags", TagViewSet, basename="tags")

ques_comments_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
ques_comments_router.register("comments", QuestionCommentViewSet, basename="ques_comments")

ans_comments_router = routers.NestedDefaultRouter(router, "answers", lookup="answer")
ans_comments_router.register("comments", AnswerCommentViewSet, basename="ans_comments")

urlpatterns = router.urls + ques_comments_router.urls + ans_comments_router.urls
