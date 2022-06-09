from django.shortcuts import render

# Create your views here.
def configurator_view(request):
    return render(request,"configurator/configurator.html",{})
