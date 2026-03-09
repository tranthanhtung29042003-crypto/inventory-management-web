from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    user = request.user
    print(user)
    return render(request, "dashboard.html", {"user": user})


@login_required
def listuserview(request):
    if request.method == "GET":
        listuser = User.objects.all()
        return render(request, "user/list_user.html", {"listuser": listuser})


    return render(request, "blank_page.html")


@login_required
def listloguser(request):
    if request.method == "GET":
        listloguser = { "sucsse"}
        return render(request, "user/user_log_activity.html", {"listuser": listloguser})

    return render(request, "blank_page.html")


