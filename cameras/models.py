from django.db import models


CODECS =(
    ("h264", "h264"),
    ("h265", "h265"),
)
# Create your models here.
class Camera(models.Model):
    name = models.CharField(max_length=30, default='')
    ip = models.GenericIPAddressField(protocol="IPv4")
    port = models.IntegerField()
    codec = models.CharField(max_length=5,choices=CODECS, default='')
    user = models.CharField(max_length=100, default='', blank=True)
    password = models.CharField(max_length=100, default='', blank=True)
    suffix = models.CharField(max_length=100, default='')