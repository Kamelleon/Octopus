import os
import traceback

from PIL import Image
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators import gzip

from .forms import CameraForm
from .models import Camera
import cv2
import threading
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import torch
import cv2, queue, threading, time

# bufferless VideoCapture
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom


# Images


class VideoCamera:
    def __init__(self, rtsp_ip):
        self.cap = cv2.VideoCapture(f"rtsp://192.168.0.104:8080/video/h264")
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def __del__(self):
        cv2.destroyAllWindows()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            # frame = cv2.resize(frame, (640, 480))
            self.q.put(frame)

    def read(self):
        return self.q.get()

    # def get_frame(self):
    #     success, imgNp = self.url.read()
    #     resize = cv2.resize(imgNp, (640, 480))
    #     ret, jpeg = cv2.imencode('.jpg', resize)
    #     return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.read()
        result = model(frame)
        rendered_image = _render_results(result)
        ret, frame = cv2.imencode('.jpg', rendered_image)
        frame = frame.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def _render_results(results):
    try:
        results.render()

        return results.imgs[0]
    except:
        print(traceback.print_exc())


@gzip.gzip_page
def rtsp_stream(request, rtsp_ip, port):
    return StreamingHttpResponse(gen(VideoCamera(rtsp_ip)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


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


def start_detector_system():
    from detector.detector_system import detector
    detector_thread = threading.Thread(target=detector.run)
    detector_thread.start()
