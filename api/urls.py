from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver
from .views import main_spa, SignUpView, UserViewSet, HobbyViewSet

# Initialize the default router
router: DefaultRouter = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"hobbies", HobbyViewSet)

# Define urlpatterns with type annotations
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("auth/", include("django.contrib.auth.urls")),  # Authentication URLs
    path("auth/signup/", SignUpView.as_view(), name="signup"),  # Signup URL
    path("api/", include(router.urls)),  # API endpoints for User and Hobby
    re_path(".*", main_spa),  # Catch-all route for the SPA
]

# Add static files configuration in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
