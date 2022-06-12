"""octopus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from login.views import login_view, logout_view
from register.views import register_view
from main_screen.views import main_screen_view
from cameras.views import cameras_preview_view, add_camera_view, camera_details_view, camera_update_view, camera_delete_view, rtsp_stream, cameras_categories_view
from detector.views import detector_calendar_view, detector_categories_view, detector_preview_view, detector_live_preview, detector_specific_preview
from configurator.views import configurator_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name='register'),
    path('cameras/', cameras_categories_view, name='cameras-categories'),
    path('cameras/preview', cameras_preview_view, name='cameras-preview'),
    path('cameras/add_camera/', add_camera_view, name='add-camera'),
    path('cameras/details/<int:camera_id>', camera_details_view, name='camera-details'),
    path('cameras/update/<int:camera_id>', camera_update_view, name='camera-update'),
    path('cameras/delete/<int:camera_id>', camera_delete_view, name='camera-delete'),
    path('cameras/rtsp_stream/<str:rtsp_ip>/<int:port>/<path:suffix>', rtsp_stream, name='rtsp-stream'),
    path('', main_screen_view, name='main-screen'),
    path('configurator/', configurator_view, name='configurator'),
    path('files/', include('directory.urls')),
    path('detector/', detector_categories_view, name='detector-categories'),
    path('detector/calendar/', detector_calendar_view, name='detector-calendar'),
    path('detector/preview/', detector_preview_view, name='detector-preview'),
    path('detector/preview/<int:camera_id>', detector_specific_preview, name='detector-specific-preview'),
    path('detector/rtsp_stream/<str:rtsp_ip>/<int:port>/<path:suffix>', detector_live_preview, name='detector-rtsp-stream'),
]
