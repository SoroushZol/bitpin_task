# Generated by Django 5.1.4 on 2024-12-27 16:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO blog_post (title, content, average_score, score_count) VALUES
            ('Post 1', 'Content for post 1', 0.00, 0),
            ('Post 2', 'Content for post 2', 0.00, 0),
            ('Post 3', 'Content for post 3', 0.00, 0),
            ('Post 4', 'Content for post 4', 0.00, 0),
            ('Post 5', 'Content for post 5', 0.00, 0),
            ('Post 6', 'Content for post 6', 0.00, 0),
            ('Post 7', 'Content for post 7', 0.00, 0),
            ('Post 8', 'Content for post 8', 0.00, 0),
            ('Post 9', 'Content for post 9', 0.00, 0),
            ('Post 10', 'Content for post 10', 0.00, 0),
            ('Post 11', 'Content for post 11', 0.00, 0),
            ('Post 12', 'Content for post 12', 0.00, 0),
            ('Post 13', 'Content for post 13', 0.00, 0),
            ('Post 14', 'Content for post 14', 0.00, 0),
            ('Post 15', 'Content for post 15', 0.00, 0),
            ('Post 16', 'Content for post 16', 0.00, 0),
            ('Post 17', 'Content for post 17', 0.00, 0),
            ('Post 18', 'Content for post 18', 0.00, 0),
            ('Post 19', 'Content for post 19', 0.00, 0),
            ('Post 20', 'Content for post 20', 0.00, 0),
            ('Post 21', 'Content for post 21', 0.00, 0),
            ('Post 22', 'Content for post 22', 0.00, 0),
            ('Post 23', 'Content for post 23', 0.00, 0),
            ('Post 24', 'Content for post 24', 0.00, 0),
            ('Post 25', 'Content for post 25', 0.00, 0),
            ('Post 26', 'Content for post 26', 0.00, 0),
            ('Post 27', 'Content for post 27', 0.00, 0),
            ('Post 28', 'Content for post 28', 0.00, 0),
            ('Post 29', 'Content for post 29', 0.00, 0),
            ('Post 30', 'Content for post 30', 0.00, 0),
            ('Post 31', 'Content for post 31', 0.00, 0),
            ('Post 32', 'Content for post 32', 0.00, 0),
            ('Post 33', 'Content for post 33', 0.00, 0),
            ('Post 34', 'Content for post 34', 0.00, 0),
            ('Post 35', 'Content for post 35', 0.00, 0),
            ('Post 36', 'Content for post 36', 0.00, 0),
            ('Post 37', 'Content for post 37', 0.00, 0),
            ('Post 38', 'Content for post 38', 0.00, 0),
            ('Post 39', 'Content for post 39', 0.00, 0),
            ('Post 40', 'Content for post 40', 0.00, 0),
            ('Post 41', 'Content for post 41', 0.00, 0),
            ('Post 42', 'Content for post 42', 0.00, 0),
            ('Post 43', 'Content for post 43', 0.00, 0),
            ('Post 44', 'Content for post 44', 0.00, 0),
            ('Post 45', 'Content for post 45', 0.00, 0),
            ('Post 46', 'Content for post 46', 0.00, 0),
            ('Post 47', 'Content for post 47', 0.00, 0),
            ('Post 48', 'Content for post 48', 0.00, 0),
            ('Post 49', 'Content for post 49', 0.00, 0),
            ('Post 50', 'Content for post 50', 0.00, 0);
        """,
                          """
                DELETE FROM blog_post
                WHERE title LIKE 'Post %' AND score_count = 0 AND average_score = 0.00
                LIMIT 50;
      """)
    ]