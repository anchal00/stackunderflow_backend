from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token routes
    path('stackunderflow/api/token', TokenObtainPairView.as_view(), name='get_token'),
    path('stackunderflow/api/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    path('stackunderflow/api/', include('stack_underflow_app.urls')),
]
