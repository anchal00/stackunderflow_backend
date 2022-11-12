from rest_framework.routers import DefaultRouter
from stack_underflow_app.apis.question_apis import QuestionViewSet
from stack_underflow_app.apis.tag_apis import TagViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = router.urls
