from django.db import transaction, models
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BlogPostFilter
from .models import BlogPost, Score
from .pagination import BlogPostPagination
from .redis_client import redis_client, _key
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, ScoreSerializer


class BlogPostViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    A viewset for creating, updating, retrieving, and listing posts
    """
    queryset = BlogPost.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogPostFilter
    pagination_class = BlogPostPagination
    search_fields = ['title', 'content']
    ordering_fields = ['average_score', 'score_count']

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        # If the user is authenticated, annotate the user's score onto each post
        request = self.request
        if request and request.user.is_authenticated:
            user_id = request.user.id
            # Use Prefetch to fetch related scores for the current user
            queryset = queryset.prefetch_related(
                models.Prefetch('scores', queryset=Score.objects.filter(user_id=user_id), to_attr='user_score')
            )

        return queryset


class AddScoreViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A viewset for creating and updating scores for a post
    """
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Score.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        new_score = serializer.validated_data['score']
        with transaction.atomic():
            # Update partial aggregates in Redis
            # we can keep track of two fields: the total sum of scores and count
            redis_key = _key.format(post.id)
            redis_client.hincrby(redis_key, "sum", new_score)
            redis_client.hincrby(redis_key, "count", 1)
            serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        post = instance.post
        new_score = serializer.validated_data['score']
        with transaction.atomic():
            redis_key = _key.format(post.id)
            redis_client.hincrby(redis_key, "sum", new_score - instance.score)
            redis_client.hincrby(redis_key, "count", 0)
            serializer.save()
