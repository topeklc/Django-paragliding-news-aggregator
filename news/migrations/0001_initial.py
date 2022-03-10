# Generated by Django 4.0.2 on 2022-03-04 16:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("author", models.CharField(blank=True, max_length=200, null=True)),
                ("date", models.DateTimeField()),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("short_description", models.TextField(blank=True, null=True)),
                ("news_link", models.CharField(blank=True, max_length=200, null=True)),
                ("image", models.ImageField(upload_to="news_images/")),
            ],
        ),
    ]
