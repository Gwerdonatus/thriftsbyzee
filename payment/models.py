from django.db import models
import uuid

class Transaction(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.PositiveIntegerField()  # In kobo
    email = models.EmailField()
    status = models.CharField(max_length=20, default='pending')  # success, failed, pending
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.reference}'
