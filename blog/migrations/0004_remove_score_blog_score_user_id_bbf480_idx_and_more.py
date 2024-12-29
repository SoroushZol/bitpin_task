# Generated by Django 5.1.4 on 2024-12-29 15:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_score_unique_together_alter_post_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='score',
            name='blog_score_user_id_bbf480_idx',
        ),
        migrations.AlterField(
            model_name='post',
            name='average_score',
            field=models.DecimalField(decimal_places=2, default=2.5, max_digits=3),
        ),
        migrations.AddIndex(
            model_name='score',
            index=models.Index(fields=['user', 'post', 'last_update'], name='blog_score_user_id_fbaff9_idx'),
        ),
    ]
