from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SiteSettingsModel(models.Model):
    siteName = models.CharField(max_length=50, verbose_name="Site Adı")
    siteDescription = models.TextField(verbose_name="Site Açıklaması")
    
    def __str__(self):
        return self.siteName
    
    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"