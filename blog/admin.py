from django.contrib import admin
from .models import Post, Score, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'average_score', 'score_count')
    search_fields = ('title', 'content')


#
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'score', 'last_update')
    list_filter = ('score', 'last_update')
    search_fields = ('post__title', 'user__username')

