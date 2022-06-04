from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators import gzip

from .forms import CameraForm
from .models import Camera
import cv2
import threading



class VideoCamera:
    def __init__(self, rtsp_ip, port):
        self.rtsp_ip = rtsp_ip
        print(rtsp_ip)
        print(port)
        print(f"rtsp://{rtsp_ip}"+":"+f"{port}/video/h264")
        self.video = cv2.VideoCapture(f"rtsp://{rtsp_ip}"+":"+f"{port}/video/h264")
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global streaming_http_response
        try:
            image = self.frame
            _, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        except:
            streaming_http_response.close()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    global streaming_http_response
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            streaming_http_response.close()
            break

streaming_http_response = StreamingHttpResponse()
@gzip.gzip_page
def rtsp_stream(request, rtsp_ip, port):
    print(rtsp_ip)
    print(port)
    global streaming_http_response
    streaming_http_response = StreamingHttpResponse()
    try:
        cam = VideoCamera(rtsp_ip, port)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


@login_required(login_url='login')
def main_screen_view(request):
    camera_objects = Camera.objects.all()
    context = {
        "camera_objects": camera_objects
    }
    return render(request, "main_screen/main_screen.html", context=context)


@login_required(login_url='login')
def add_camera_view(request):
    form = CameraForm()
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main-screen")

    context = {
        "form": form
    }
    return render(request, "main_screen/add_camera.html", context=context)


@login_required(login_url='login')
def camera_details_view(request, camera_id):
    context = {
        "camera_object": get_object_or_404(Camera.objects.all(), id=camera_id)
    }
    return render(request, "main_screen/camera_details.html", context=context)


@login_required(login_url='login')
def camera_update_view(request, camera_id):
    obj = get_object_or_404(Camera, id=camera_id)
    form = CameraForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect("camera-details", camera_id=camera_id)

    context = {
        "form": form
    }
    return render(request, "main_screen/camera_update.html", context=context)


@login_required(login_url='login')
def camera_delete_view(request, camera_id):
    obj = get_object_or_404(Camera, id=camera_id)

    if request.method == "POST":
        obj.delete()
        return redirect("main-screen")

    return redirect('main-screen')


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, "main_screen/dashboard.html", {})