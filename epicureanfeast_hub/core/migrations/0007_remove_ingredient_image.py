# Generated by Django 5.0.1 on 2024-01-18 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_remove_recipebook_likes_recipebook_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ingredient",
            name="image",
        ),
    ]
