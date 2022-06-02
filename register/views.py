from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
# Create your views here.
from django.views import View
from django.contrib import messages

def register_view(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,f"Account created successfully for {user}")
            return redirect("login")

    context = {'form':form}
    return render(request,"register/register.html",context=context)