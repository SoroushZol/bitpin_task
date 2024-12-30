from rest_framework import serializers

from blog.models import BlogPost, Score


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Score
        fields = ['user', 'post', 'score', 'last_update']


class BlogPostListSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')

    class Meta:
        model = BlogPost
        fields = ['title', 'average_score', 'score_count', 'detail_url', 'user_score']
        read_only_fields = ['average_score', 'score_count']

    def get_user_score(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        user = request.user

        # Fetch the user's score for this post, if it exists
        score = next((s for s in obj.user_score if s.user_id == user.id), None)
        return ScoreSerializer(score).data if score else {}


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'average_score', 'score_count']

    average_score = serializers.ReadOnlyField()
    score_count = serializers.ReadOnlyField()
