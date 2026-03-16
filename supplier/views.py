from django.shortcuts import render, get_object_or_404, redirect


from supplier.models import Supplier


# Create your views here.
def supplier_page(request):

    suppliers = Supplier.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        tax_code = request.POST.get("tax_code")
        Supplier.objects.create(name=name, phone=phone, email=email, address=address, tax_code=tax_code)
        return redirect("supplier_page")

    return render(request, "supplier/supplier_page.html", {"suppliers": suppliers})

def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    supplier.delete()

    return redirect("supplier_page")

def update_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    if request.method == "POST":
        supplier.name = request.POST.get("name")
        supplier.phone = request.POST.get("phone")
        supplier.email = request.POST.get("email")
        supplier.address = request.POST.get("address")
        supplier.tax_code = request.POST.get("tax_code")

        supplier.save()
        return redirect("supplier_page")
    return render(request, "supplier/update_supplier.html", {"supplier": supplier})

