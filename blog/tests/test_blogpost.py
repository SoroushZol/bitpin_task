import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import BlogPost, Score
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestBlogPost:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.blog_post = BlogPost.objects.filter(title='Post 1').first()

    def test_list_blog_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['title'] == 'Post 1'

    def test_retrieve_blog_post(self):
        url = reverse('post-detail', args=[self.blog_post.pk])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Post 1'

    def test_update_blog_post(self):
        url = reverse('post-detail', args=[self.blog_post.pk])
        data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.blog_post.refresh_from_db()
        assert self.blog_post.title == 'Updated Post'
        assert self.blog_post.content == 'Updated Content'

    def test_user_score_retrieval(self):
        Score.objects.create(user=self.user, post=self.blog_post, score=4)
        url = reverse('post-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['user_score']['score'] == 4
