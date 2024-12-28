from django_filters.rest_framework import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'average_score': ['gt', 'lt'],
            'score_count': ['gt', 'lt'],
        }

