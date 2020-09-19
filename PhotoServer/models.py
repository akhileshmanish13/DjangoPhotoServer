from django.db import models
# from datetime import datetime
from django.utils import timezone

class CachedPhoto(models.Model):
    cached_image = models.BinaryField(blank=True, null=True)
    cache_file_url = models.CharField(max_length=500, null=True)

    #Default values
    number_of_times_read = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    
