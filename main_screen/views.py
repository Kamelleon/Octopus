from django.shortcuts import render

# Create your views here.
def main_screen_view(request):
    return render(request,"main_screen/main_screen.html",{})