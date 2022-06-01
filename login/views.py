from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginView(View):
    def get(self,request):
        context = {}
        return render(request, "login/login.html", context=context)