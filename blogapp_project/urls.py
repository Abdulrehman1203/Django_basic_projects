from django.contrib import admin
from django.urls import path, include
from blogapp import urls as blog_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views as auth_views

"""These url patterns are listed below:"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(blog_urls)),
    path('blogging_app/', include('django.contrib.auth.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', auth_views.obtain_auth_token),
]
