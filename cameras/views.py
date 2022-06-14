import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CameraForm
from .models import Camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2, queue, threading
import rtsp
from camera_capturer.rtsp_capturer import  Capturer

import threading


# class StoppableThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""
#
#     def __init__(self,  *args, **kwargs):
#         super(StoppableThread, self).__init__(*args, **kwargs)
#         self._stop_event = threading.Event()
#
#     def stop(self):
#         self._stop_event.set()
#
#     def stopped(self):
#         return self._stop_event.is_set()
#
# class VideoCamera:
#     def __init__(self, rtsp_ip, port, suffix):
#         self.cap = cv2.VideoCapture(f"rtsp://{rtsp_ip}:{port}{suffix}")
#         self.q = queue.Queue()
#         self.t = StoppableThread(target=self._reader)
#         self.t.daemon = True
#         self.t.start()
#
#     def __del__(self):
#         print("deleting")
#         self.cap.release()
#         # cv2.destroyAllWindows()
#
#     def _reader(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("No ret, releasing...")
#                 self.cap.release()
#                 break
#             if not self.q.empty():
#                 try:
#                     self.q.get_nowait()
#                 except queue.Empty:
#                     pass
#             self.q.put(frame)
#
#     def read(self):
#         return self.q.get()
#
#     def preprocess(self, frame):
#         ret, frame = cv2.imencode('.jpg', frame)
#         return frame
from imutils.video import VideoStream


#
def gen(camera_capturer):
    while True:
        frame = camera_capturer.get_frame()
        print("Getting frame")
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            # del camera_capturer
            break




def generate(capturer):
        while True:
            time.sleep(0.1)
            with capturer.lock:
                if capturer.outputFrame is None:
                    continue

                flag, encodedImage = cv2.imencode(".jpg", capturer.outputFrame)

                if not flag:
                    continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encodedImage.tobytes() + b'\r\n\r\n')




@gzip.gzip_page
def rtsp_stream(request, rtsp_ip, port, suffix):
    # camera_capturer.close_client_if_opened()
    # video_camera = VideoCamera(rtsp_ip, port, suffix)
    # camera_capturer = CameraCapturer(rtsp_ip, port, suffix)
    print(Capturer.generators)
    print(Capturer.restricted)
    if rtsp_ip not in Capturer.restricted:
        capturer = Capturer(rtsp_ip, port, suffix)
        Capturer.generators.append(dict({f"{rtsp_ip}":capturer}))
        Capturer.restricted.append(rtsp_ip)
        return StreamingHttpResponse(capturer.generate(),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    for camera_object in Capturer.generators:
        if rtsp_ip in camera_object.keys():
            camera_generator = camera_object[rtsp_ip]
            return StreamingHttpResponse(camera_generator.generate(),
                                         content_type='multipart/x-mixed-replace; boundary=frame')



@login_required(login_url='login')
def cameras_categories_view(request):
    return render(request, "cameras/cameras_categories.html", {})


@login_required(login_url='login')
def cameras_preview_view(request):
    cv2.destroyAllWindows()
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
