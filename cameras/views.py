import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CameraForm
from .models import Camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2, queue, threading
import rtsp


class VideoCamera:
    def __init__(self, rtsp_ip, port, suffix):
        self.cap = cv2.VideoCapture(f"rtsp://{rtsp_ip}:{port}{suffix}")
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # def __del__(self):
    #     print("deleting")
    #     self.cap.release()
    #     # cv2.destroyAllWindows()
    #
    # def _reader(self):
    #     while True:
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             print("No ret, releasing...")
    #             self.cap.release()
    #             break
    #         if not self.q.empty():
    #             try:
    #                 self.q.get_nowait()
    #             except queue.Empty:
    #                 pass
    #         self.q.put(frame)
    #
    # def read(self):
    #     return self.q.get()

    def preprocess(self, frame):
        ret, frame = cv2.imencode('.jpg', frame)
        return frame


def gen():
    client = rtsp.Client(rtsp_server_uri = 'rtsp://192.168.0.103:8080/video/h264')
    time.sleep(0.2)
    while client.isOpened():
        _image = client.read(raw=True)
        ret, frame = cv2.imencode('.jpg', _image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')


@login_required(login_url='login')
@gzip.gzip_page
def rtsp_stream(request, rtsp_ip, port, suffix):
    print("Getting stream")
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def cameras_categories_view(request):
    return render(request,"cameras/cameras_categories.html",{})


@login_required(login_url='login')
def cameras_preview_view(request):
    camera_objects = Camera.objects.all()
    context = {
        "camera_objects": camera_objects
    }
    return render(request, "cameras/cameras_preview.html", context=context)


@login_required(login_url='login')
def add_camera_view(request):
    form = CameraForm()
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cameras-preview")

    context = {
        "form": form
    }
    return render(request, "cameras/camera_add.html", context=context)


@login_required(login_url='login')
def camera_details_view(request, camera_id):
    context = {
        "camera_object": get_object_or_404(Camera.objects.all(), id=camera_id)
    }
    return render(request, "cameras/camera_details.html", context=context)


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
    return render(request, "cameras/camera_update.html", context=context)


@login_required(login_url='login')
def camera_delete_view(request, camera_id):
    obj = get_object_or_404(Camera, id=camera_id)

    if request.method == "POST":
        obj.delete()
        return redirect("cameras-preview")

    return redirect('cameras-preview')

