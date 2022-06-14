import datetime
import os
import re

from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators import gzip

from cameras.models import Camera
from detector.live_preview import generate_live_detector_preview
# from cameras.views import VideoCamera
# from camera_capturer.rtsp_capturer import CameraCapturer


@login_required(login_url='login')
def detector_specific_preview(request, camera_id):
    camera_objects = Camera.objects.all()
    context = {
        "camera_objects": camera_objects,
        "selected_camera": get_object_or_404(Camera.objects.all(), id=camera_id)
    }
    print(context)
    return render(request, "detector/detector_specific_preview.html", context=context)

@login_required(login_url='login')
def detector_preview_view(request):
    camera_objects = Camera.objects.all()
    context = {
        "camera_objects": camera_objects
    }
    return render(request, "detector/detector_preview.html", context=context)

@gzip.gzip_page
def detector_live_preview(request, rtsp_ip, port, suffix):
    camera_capturer.close_client_if_opened()
    return StreamingHttpResponse(camera_capturer.gen(rtsp_ip, port, suffix),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def detector_categories_view(request):
    return render(request, "detector/detector_categories.html", {})


@login_required(login_url='login')
def detector_calendar_view(request):
    directories_with_dates = []
    dirs_list = os.listdir(os.getcwd())
    for directory in dirs_list:
        if re.match(".{2}-.{2}-.{4}", directory):
            directories_with_dates.append(directory)
    directories_with_dates.sort(key=lambda date: datetime.datetime.strptime(date, '%d-%m-%Y'))
    context = {
        "directories_with_dates":directories_with_dates
    }
    return render(request, "detector/detector_calendar.html", context=context)


# def start_detector_system():
#     from detector.detector_system import detector
#     detector_thread = threading.Thread(target=detector.run)
#     detector_thread.start()
