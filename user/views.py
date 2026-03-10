from django.utils import timezone

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import User
from .services.check_exits_email import check_exist_email
from .services.check_exits_username import check_exist_username


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


@login_required
def edit_user(request, id):

    user = get_object_or_404(User, id=id)
    print(request)
    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:

            user.email = request.POST.get("email")
            user.phone = request.POST.get("phone")
            user.role = request.POST.get("role")

            if password:
                user.set_password(password)

            user.updated_at = timezone.now()
            user.save()

            return redirect("listuserview")

    return render(request, "user/edit_info_user.html", {"user": user})



@login_required
def add_new_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        print(username, email, phone, password, confirm_password, role)
        check_exist_email(email)
        check_exist_username(username)

        if password != confirm_password:
            return render(request, "user/add_new_user.html", {
                "error": "Password không khớp"
            })
        User.objects.create_user(username=username, email=email, phone=phone, password=password, role=role)

        return redirect("listuserview")

    return render(request, "user/add_new_user.html")



@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "Delete":
        user.delete()
        return redirect("dashboard")

    return render(request, "user/dashboard.html")