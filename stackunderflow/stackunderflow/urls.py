from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token')
]
