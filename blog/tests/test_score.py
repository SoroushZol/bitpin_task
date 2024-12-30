import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import BlogPost, Score
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestScore:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.blog_post = BlogPost.objects.filter(title='Post 1').first()

    def test_create_score(self):
        url = reverse('score-list')
        data = {'post': self.blog_post.id, 'score': 4}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['score'] == 4
        assert response.data['post'] == self.blog_post.id

    def test_update_score(self):
        score = Score.objects.create(user=self.user, post=self.blog_post, score=3)
        url = reverse('score-detail', args=[score.id])
        data = {'post': self.blog_post.id, 'score': 5}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        score.refresh_from_db()
        assert score.score == 5

    def test_retrieve_score(self):
        score = Score.objects.create(user=self.user, post=self.blog_post, score=3)
        url = reverse('score-detail', args=[score.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
