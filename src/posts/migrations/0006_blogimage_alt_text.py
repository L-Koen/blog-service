# Generated by Django 5.1.6 on 2025-02-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_keyword_post_keywords"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogimage",
            name="alt_text",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
