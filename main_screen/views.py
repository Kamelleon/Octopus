from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CameraForm
from .models import Camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2, queue, threading


class VideoCamera:
    def __init__(self, rtsp_ip, port, suffix):
        self.cap = cv2.VideoCapture(f"rtsp://{rtsp_ip}:{port}{suffix}")
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def __del__(self):
        cv2.destroyAllWindows()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def gen(camera):
    while True:
        frame = camera.read()
        ret, frame = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')


@login_required(login_url='login')
@gzip.gzip_page
def rtsp_stream(request, rtsp_ip, port, suffix):
    return StreamingHttpResponse(gen(VideoCamera(rtsp_ip, port, suffix)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def main_screen_view(request):
    camera_objects = Camera.objects.all()
    context = {
        "camera_objects": camera_objects
    }
    return render(request, "main_screen/cameras_view.html", context=context)


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
    return render(request, "main_screen/camera_add.html", context=context)


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
