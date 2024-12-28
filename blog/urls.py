from django.urls import path, include
from blog.views import PostViewSet, AddScoreViewSet
from rest_framework.routers import DefaultRouter
from pprint import pprint

router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('score', AddScoreViewSet, basename='score')

urlpatterns = [
    path('', include(router.urls)),
]
