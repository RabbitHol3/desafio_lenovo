from django.db import models
from asgiref.sync import sync_to_async
from django.conf import settings
from utils.connect_db import init_django
from django.utils import timezone

init_django()

class Product(models.Model):
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)
    description = models.TextField()
    memory = models.CharField(max_length=100)
    ratings = models.CharField(max_length=7)
    size = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def save(self, *args, **kwargs):
        #update at
        if self.pk:
            self.updated_at = timezone.now()
        return super(Product, self).save(*args, **kwargs)
        
    
    class Meta:
        ordering = ('name',)
        unique_together = ('name','value', 'size')
        
    
    
