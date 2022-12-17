from rest_framework.routers import DefaultRouter
from stack_underflow_app.apis.answer_apis import AnswerViewSet
from stack_underflow_app.apis.comment_apis import (AnswerCommentViewSet,
                                                   QuestionCommentViewSet)
from stack_underflow_app.apis.question_apis import QuestionViewSet
from stack_underflow_app.apis.tag_apis import TagViewSet

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
router.register("answers", AnswerViewSet, basename="answers")
router.register("tags", TagViewSet, basename="tags")
router.register("question_comments", QuestionCommentViewSet, basename="ques_comments")
router.register("answer_comments", AnswerCommentViewSet, basename="ans_comments")

urlpatterns = router.urls
