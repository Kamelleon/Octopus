from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('main-screen')
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, "login/login.html", context=context)

def logout_view(request):
    logout(request)
    return redirect('login')