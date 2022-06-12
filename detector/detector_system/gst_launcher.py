import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "octopus.settings")
import django
django.setup()
from cameras.models import Camera

all_cameras = Camera.objects.all()
all_cameras = all_cameras.values()
for camera_object in all_cameras:
    ip = camera_object['ip']
    port = camera_object['port']
    name = camera_object['name']
    user = camera_object['user']
    password = camera_object['password']
    codec = camera_object['codec']
    suffix = camera_object['suffix']
    print(ip,port,name,user,password,codec, suffix)



# def create_gst_script(ip,port,name,codec):
#     if user == "":
#         gst_launch_command = 'gst-launch-1.0 rtspsrc location="rtsp://192.168.0.103:8080/video/h264" ! rtph264depay ! avdec_h264 ! videorate ! video/x-raw,framerate=2/1 ! jpegenc ! multifilesink location=kamera.jpg'