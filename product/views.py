from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
import openpyxl
from django.http import HttpResponse
from django.utils import timezone


from category.models import Category
from product.models import Product
from product.forms import ProductForm

# Create your views here.


def add_product(request):

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect("product_list")

    else:
        form = ProductForm()

    return render(request, "product/add_new_product.html", {"form": form, "categories": Category.objects.all()})


def product_list(request):
    search = request.GET.get("search")
    category_id = request.GET.get("category")

    products = Product.objects.all().order_by("-created_at")
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search)
        )

    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()

    return render(request, "product/list_product.html", {"listproduct": products,   "categories": categories})

def delete_product(request, id):
    product = get_object_or_404(Product,id = id)
    product.delete()
    return redirect("product_list")

def update_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.sku = request.POST.get("sku")

        category_id = request.POST.get("category")
        product.category = Category.objects.get(id=category_id)

        product.import_price = request.POST.get("import_price")
        product.sell_price = request.POST.get("sell_price")
        product.quantity_in_stock = request.POST.get("quantity_in_stock")
        product.min_stock_level = request.POST.get("min_stock_level")

        image = request.FILES.get("image")
        if image:
            product.image = image

        product.save()

        return redirect("product_list")

    categories = Category.objects.all()

    return render(
        request,
        "product/update_product.html",
        {
            "product": product,
            "categories": categories
        }
    )


def export_product_excel(request):
    products = Product.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Products"

    # Header
    sheet.append(["ID", "Name", "SKU", "Category", "Import Price", "Sell Price", "Quantity", "Min Stock", "Image","Created at", "Updated at"])

    # Data
    for p in products:
        sheet.append([
            p.id,
            p.name,
            p.sku,
            p.category.name if p.category else "",  # Tránh lỗi nếu category bị None
            p.import_price,
            p.sell_price,
            p.quantity_in_stock,
            p.min_stock_level,
            p.image.url if p.image else "",
            p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            p.updated_at.strftime("%Y-%m-%d %H:%M:%S")


        ])


    current_time = timezone.now().strftime("%Y%m%d_%H%M")
    filename = "products_{}.xlsx".format(current_time)


    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    workbook.save(response)

    return response