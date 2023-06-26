from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()

    def __str__(self):
        return self.title
