# Generated by Django 5.1.6 on 2025-02-11 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="body",
            new_name="content",
        ),
        migrations.RemoveField(
            model_name="post",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="post",
            name="updated_at",
        ),
    ]
