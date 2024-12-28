from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Post model
class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    average_score = models.DecimalField(max_digits=3, decimal_places=2,  default=0.0)  # To store the average score
    score_count = models.IntegerField(default=0)  # To store the number of scores

    def __str__(self):
        return self.title

    def calculate_average(self, new_score):
        """
        Dynamically calculate the average score when a new score is added.
        """
        total_score = self.average_score * self.score_count + new_score
        self.score_count += 1
        self.average_score = total_score / self.score_count

    def update_average_from_cache(self, total_weighted_score, total_weight, score_count):
        """
        Update the average score and count from the cache syncing process.
        """
        self.average_score = total_weighted_score / total_weight if total_weight > 0 else 0
        self.score_count += score_count


# Score model
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # Should be between 0 and 5
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Prevent duplicate ratings by the same user on the same post
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]
        indexes = [
            models.Index(fields=['user', 'post']),  # Optimize lookups
        ]

    def __str__(self):
        return f"Score {self.score} by {self.user.username} for {self.post.title}"
