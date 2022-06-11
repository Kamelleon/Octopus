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
from main_screen.views import main_screen_view, add_camera_view, camera_details_view, camera_update_view, camera_delete_view, rtsp_stream, dashboard_view
from detector.views import detector_calendar_view, detector_view
from configurator.views import configurator_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name='register'),
    path('main_screen/', main_screen_view, name='main-screen'),
    path('', dashboard_view, name='dashboard'),
    path('configurator/', configurator_view, name='configurator'),
    path('files/', include('directory.urls')),
    path('add_camera/', add_camera_view, name='add-camera'),
    path('detector/', detector_view, name='detector'),
    path('detector/calendar/', detector_calendar_view, name='detector-calendar'),
    path('camera_details/<int:camera_id>', camera_details_view, name='camera-details'),
    path('camera_update/<int:camera_id>', camera_update_view, name='camera-update'),
    path('camera_delete/<int:camera_id>', camera_delete_view, name='camera-delete'),
    path('rtsp_stream/<str:rtsp_ip>/<int:port>/<path:suffix>', rtsp_stream, name='rtsp-stream'),
]
