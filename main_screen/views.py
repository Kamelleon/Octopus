from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def main_screen_view(request):
    return render(request,"main_screen/main_screen.html",{})