from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# BlogPost model
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    average_score = models.DecimalField(max_digits=3, decimal_places=2,  default=2.5)  # To store the average score
    score_count = models.IntegerField(default=0)  # To store the number of scores

    def __str__(self):
        return self.title


# Score model
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # Should be between 0 and 5
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Prevent duplicate ratings by the same user on the same post
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]
        indexes = [
            models.Index(fields=['user', 'post', 'last_update']),  # Optimize lookups
        ]

    def __str__(self):
        return f"Score {self.score} by {self.user.username} for {self.post.title}"
