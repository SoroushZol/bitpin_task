from django.urls import path, include
from blog.views import BlogPostViewSet, AddScoreViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', BlogPostViewSet, basename='post')
router.register('score', AddScoreViewSet, basename='score')

urlpatterns = [
    path('', include(router.urls)),
]
