from rest_framework_nested import routers
from stack_underflow_app.apis.answer_apis import AnswerViewSet
from stack_underflow_app.apis.comment_apis import (AnswerCommentViewSet,
                                                   QuestionCommentViewSet)
from stack_underflow_app.apis.question_apis import QuestionViewSet
from stack_underflow_app.apis.tag_apis import TagViewSet

router = routers.DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
router.register("tags", TagViewSet, basename="tags")

# For Question's comments
ques_comments_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
ques_comments_router.register("comments", QuestionCommentViewSet, basename="ques_comments")
# For Question's answers
ques_ans_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
ques_ans_router.register("answers", AnswerViewSet, basename="ques_answers")
# For Answer's comments
ans_comments_router = routers.NestedDefaultRouter(ques_ans_router, "answers", lookup="answer")
ans_comments_router.register("comments", AnswerCommentViewSet, basename="ans_comments")

urlpatterns = router.urls + ques_comments_router.urls + ques_ans_router.urls + ans_comments_router.urls
