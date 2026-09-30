import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_photo, validate_receipt


class Event(models.Model):
    title = models.CharField(max_length=150)
    event_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'title']

    def __str__(self):
        return self.title


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    transaction_id = models.CharField(max_length=100, unique=True)
    receipt = models.FileField(upload_to='receipts/', validators=[validate_receipt])
    photo = models.ImageField(upload_to='photos/', validators=[validate_photo])
    attendance = models.BooleanField(default=False)
    feedback_given = models.BooleanField(default=False)
    feedback_text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    marks = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    certificate_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event', '-created_at']),
            models.Index(fields=['attendance']),
        ]

    def __str__(self):
        return f'{self.name} - {self.event}'

    def is_eligible(self):
        return self.attendance and self.feedback_given and self.marks is not None
