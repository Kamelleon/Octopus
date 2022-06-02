from django.forms import ModelForm, CharField, PasswordInput
from .models import Camera

class CameraForm(ModelForm):
    # password = CharField(widget=PasswordInput())
    class Meta:
        model = Camera
        fields = ["name","ip","codec","user","password","substream"]