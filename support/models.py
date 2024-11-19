from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Announcement {self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.customer_name}"

