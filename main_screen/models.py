from django.db import models


CODECS =(
    ("1", "h264"),
    ("2", "h265"),
)
# Create your models here.
class Camera(models.Model):
    name = models.CharField(max_length=30)
    ip = models.GenericIPAddressField(protocol="IPv4")
    codec = models.CharField(max_length=1, choices=CODECS)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    substream = models.BooleanField(default=False)
