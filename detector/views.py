import datetime
import os
import re

from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

from detector.live_preview import generate_live_detector_preview
from main_screen.views import VideoCamera


@login_required(login_url='login')
@gzip.gzip_page
def detector_live_preview(request, rtsp_ip, port, suffix):
    return StreamingHttpResponse(generate_live_detector_preview(VideoCamera(rtsp_ip, port, suffix)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def detector_categories_view(request):
    return render(request, "detector/detector.html", {})


@login_required(login_url='login')
def detector_calendar_view(request):
    directories_with_dates = []
    dirs_list = os.listdir(os.getcwd())
    print(dirs_list)
    for directory in dirs_list:
        if re.match(".{2}-.{2}-.{4}", directory):
            directories_with_dates.append(directory)
    directories_with_dates.sort(key=lambda date: datetime.datetime.strptime(date, '%d-%m-%Y'))
    context = {
        "directories_with_dates":directories_with_dates
    }
    print(directories_with_dates)
    return render(request, "detector/detector_calendar.html", context=context)
