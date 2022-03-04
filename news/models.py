from django.db import models
import uuid

# Create your models here.


class NewsPost(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    author = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=15, blank=True, null=True)
    epoch = models.PositiveBigIntegerField(blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    news_link = models.CharField(max_length=200, blank=True, null=True)
    media_link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-epoch"]
        unique_together = ["title"]
