from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from rest_framework.response import Response
from .models import Post, Score, User
from .pagination import PostPagination
from .serializers import PostListSerializer, PostDetailSerializer, ScoreSerializer
from django.shortcuts import get_object_or_404


class PostViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    A viewset for creating, updating, retrieving, and listing posts
    """
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    pagination_class = PostPagination
    search_fields = ['title', 'content']
    ordering_fields = ['average_score', 'score_count']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class AddScoreViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A viewset for creating and updating scores for a post
    """
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Add a score to a post.
        """
        score_data = ScoreSerializer(data=request.data)
        score_data.is_valid(raise_exception=True)

        user = get_object_or_404(User, pk=score_data.validated_data['user'])
        post = get_object_or_404(Post, pk=score_data.validated_data['post'])

        score_instance, created = Score.objects.get_or_create(user=user, post=post)
        score_instance.score = score_data.validated_data['score']
        score_instance.save()

        post.calculate_average(score_instance.score)
        post.save()

        return Response({'message': 'Score added successfully!'}, status=status.HTTP_201_CREATED)
