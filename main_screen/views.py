from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CameraForm
from .models import Camera


# Create your views here.

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
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Camera, id=camera_id)

    # pass the object as instance in form
    form = CameraForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("camera-details",camera_id=camera_id)

    # add form dictionary to context
    context = {
        "form":form
    }
    return render(request, "main_screen/camera_update.html", context=context)


@login_required(login_url='login')
def camera_delete_view(request, camera_id):
    obj = get_object_or_404(Camera, id=camera_id)

    if request.method == "POST":
        obj.delete()
        return redirect("main-screen")

    return redirect('main-screen')