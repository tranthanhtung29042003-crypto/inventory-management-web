from django.shortcuts import render, redirect, get_object_or_404

from category.models import Category
from product.models import Product


# Create your views here.

def add_product(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        if Product.objects.filter(sku=sku).exists():
            raise "Product already exist"
        name = request.POST.get('name')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        unit = request.POST.get('unit')
        import_price = request.POST.get('import_price')
        sell_price = request.POST.get('sell_price')
        quantity_in_stock = request.POST.get('quantity_in_stock')
        min_stock = request.POST.get('min_stock')
        image = request.FILES.get('image')


        Product.objects.create(name=name, price=price, sku=sku, quantity=quantity, category=category, unit=unit,
                               import_price=import_price,sell_price=sell_price, quantity_in_stock=quantity_in_stock, min_stock=min_stock,
                               image=image
                               )
        return redirect("product_list")
    categories = Category.objects.all()
    return render(request, "product/add_new_product.html", {"categories": categories})

def product_list(request):
    products = Product.objects.all()
    return render(request, "product/list_product.html", {"products": products})

def delete_product(request, product_id):
    product = get_object_or_404(Product,id = product_id)
    product.delete()
    return redirect("product_list")

def update_product(request, product_id):
    product = get_object_or_404(Product, id = product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.quantity = request.POST.get('quantity')
        product.category = request.POST.get('category')
        product.unit = request.POST.get('unit')
        product.import_price = request.POST.get('import_price')
        product.sell_price = request.POST.get('sell_price')
        product.quantity_in_stock = request.POST.get('quantity_in_stock')
        product.min_stock = request.POST.get('min_stock')
        product.image = request.FILES.get('image')
        product.save()

        return redirect("product_list")
    categories = Category.objects.all()
    return render(request, "product/update_product.html", {"product": product, "categories": categories})
