import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "octopus.settings")
import django
django.setup()
from main_screen.models import Camera

all_cameras = Camera.objects.all()
all_cameras = all_cameras.values()
for camera_object in all_cameras:
    ip = camera_object['ip']
    port = camera_object['port']
    name = camera_object['name']
    user = camera_object['user']
    password = camera_object['password']
    use_substream = camera_object['substream']
    print(ip,port,name,user,password, use_substream)



def create_gst_script(ip,port,name,codec):
    pass
    # if user == "":
        # gst_launch_command =