from rest_framework import serializers
from .redis_client import get_redis_post_data
from blog.models import BlogPost, Score


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Score
        fields = ['id', 'user', 'post', 'score', 'last_update']


class BlogPostListSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'average_score', 'score_count', 'detail_url', 'user_score']
        read_only_fields = ['average_score', 'score_count']

    def get_user_score(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        user = request.user
        # Fetch the user's score for this post, if it exists
        score = next((s for s in obj.user_score if s.user_id == user.id), None)
        return ScoreSerializer(score).data if score else {}

    def get_score_count(self, obj):
        data = get_redis_post_data(obj.id)
        if not data:
            return obj.score_count
        new_count = int(data["count"])
        return obj.score_count + new_count

    def get_average_score(self, obj):
        data = get_redis_post_data(obj.id)
        if not data:
            return obj.average_score
        new_sum = int(data["sum"])
        new_count = int(data["count"])
        if new_count == 0:
            new_avg = new_sum
        else:
            new_avg = new_sum / new_count
            new_count = 1
        old_avg = float(obj.average_score)
        old_count = obj.score_count
        new_weighted_avg = ((old_avg * old_count) + new_avg) / (old_count + new_count)
        return new_weighted_avg


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'average_score', 'score_count']

    average_score = serializers.ReadOnlyField()
    score_count = serializers.ReadOnlyField()
