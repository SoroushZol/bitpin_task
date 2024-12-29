from celery import shared_task
from .models import Post
from .redis_client import redis_client


@shared_task
def aggregate_scores():
    """
    Aggregates partial scores from Redis for each post,
    and updates the Post table in bulk.
    """

    cursor = 0
    keys = []
    while True:
        cursor, batch_keys = redis_client.scan(cursor=cursor, match="post:*:scores", count=100)
        keys.extend(batch_keys)
        if cursor == 0:
            break

    # We'll parse each key => post_id
    for key in keys:
        # Example key format: "post:123:scores"
        try:
            post_id = int(key.split(":")[1])
        except (IndexError, ValueError):
            # Skip malformed keys
            continue

        # Grab the "sum" and "count" from Redis
        data = redis_client.hgetall(key)
        # data should look like {"sum": "<some_value>", "count": "<some_value>"}
        if not data or "sum" not in data or "count" not in data:
            continue

        new_sum = int(data["sum"])
        new_count = int(data["count"])

        if new_count == 0:
            # Nothing to aggregate
            continue

        # Retrieve the existing Post from DB
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            # Clean up Redis if post doesn't exist
            redis_client.delete(key)
            continue

        # Compute the average of the new scores
        new_avg = new_sum / new_count

        # Merge with existing post average using Weighted Average
        # Weighted average = (old_avg * old_count + new_avg * 1) / (old_count + 1)
        # The new_count is always 1, because we aggregate the scores to reduce their effect in short term

        old_avg = float(post.average_score)
        old_count = post.score_count

        # Weighted average of old and new
        new_weighted_avg = ((old_avg * old_count) + (new_avg * new_count)) / old_count + 1

        # Update the Post fields
        post.average_score = round(new_weighted_avg, 2)
        post.score_count = old_count + new_count
        post.save()

        # 6) Clear or reset the partial aggregates in Redis so that next time we only process new data
        redis_client.delete(key)

    return "Aggregation complete."
