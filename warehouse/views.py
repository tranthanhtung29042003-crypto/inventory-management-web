from django.utils import timezone

from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Warehouse
from user.views import role_required


def warehouse_page(request):

    warehouse = Warehouse.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")

        Warehouse.objects.create(name=name, address=address)
        return redirect("warehouse_page")

    return render(request, "warehouse/warehouse.html", {"warehouse": warehouse})
@role_required(["ADMIN", "MANAGER","ACCOUNTANT"])
@login_required
def delete_warehouse(request, id):
    warehouse = get_object_or_404(Warehouse, pk=id)
    warehouse.delete()

    return redirect("warehouse_page")
@role_required(["ADMIN", "MANAGER","ACCOUNTANT"])
@login_required
def update_warehouse(request, id):
    warehouse = get_object_or_404(Warehouse, pk=id)

    if request.method == "POST":
        warehouse.name = request.POST.get("name")


        warehouse.address = request.POST.get("address")


        warehouse.save()
        return redirect("warehouse_page")
    return render(request, "warehouse/update_warehouse.html", {"warehouse": warehouse})

