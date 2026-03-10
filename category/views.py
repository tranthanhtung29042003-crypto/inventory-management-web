from django.utils import timezone

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Category


@login_required
def listcagegoryview(request):
    if request.method == "GET":
        listcategory = Category.objects.all()
        return render(request, "category/list_category.html", {"listcategory": listcategory})


    return render(request, "blank_page.html")

@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST.get("name")
        parent_id = request.POST.get("parent")
        description = request.POST.get("description")

        parent = None

        if parent_id:
            parent = Category.objects.get(id=parent_id)

        Category.objects.create(
            name=name,
            parent=parent,
            description=description
        )

    categories = Category.objects.all()

    return render(request, "category/list_category.html")




@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "Delete":
        category.delete()
        return redirect("listcagegoryview")

    return render(request, "category/list_category.html")