import datetime
import os
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login')
def detector_view(request):
    return render(request, "detector/detector.html", {})

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
