from rest_framework import serializers

from blog.models import Post, Score


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'average_score', 'score_count', 'detail_url']

    detail_url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')
    # make the average_score and score_count fields read-only
    average_score = serializers.ReadOnlyField()
    score_count = serializers.ReadOnlyField()


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'average_score', 'score_count']

    average_score = serializers.ReadOnlyField()
    score_count = serializers.ReadOnlyField()


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['user', 'post', 'score', 'last_update']
