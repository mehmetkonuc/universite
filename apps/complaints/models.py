from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Complaint(models.Model):
    COMPLAINT_CATEGORIES = [
        ('spam', 'Spam/Istenmeyen İçerik'),
        ('nudity', 'Müstehcen İçerik'),
        ('hate', 'Nefret Söylemi'),
        ('violence', 'Şiddet İçeriği'),
        ('harassment', 'Taciz'),
        ('false', 'Yanlış Bilgi'),
        ('other', 'Diğer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('under_review', 'İncelemede'),
        ('resolved', 'Çözüldü'),
        ('rejected', 'Reddedildi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    category = models.CharField(max_length=20, choices=COMPLAINT_CATEGORIES)
    description = models.TextField(max_length=1000)
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
        verbose_name = 'Şikayet'
        verbose_name_plural = 'Şikayetler'
        
    def __str__(self):
        return f"{self.user.username} -> {self.content_object} ({self.get_status_display()})"