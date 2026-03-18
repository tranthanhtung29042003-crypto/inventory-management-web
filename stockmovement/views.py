from django.shortcuts import render, redirect

from product.models import Product
from stockmovement.models import StockMovement


# Create your views here.

def stock_history(request, id):
    histories = StockMovement.objects.select_related('product').order_by('-created_at')
    return render(request, 'stock_history.html', {'histories': histories})


def import_product(request, id):
    product = Product.objects.get(id=id)
    qty = int(request.POST.get('qty'))

    product.quantity_in_stock += qty
    product.save()

    StockMovement.objects.create(
        product=product,
        qty=qty,
        movement_type = 'IMPORT',
        note = "Nhập kho",

    )
    return redirect('')

def export_product(request, id):
    product = Product.objects.get(id=id)
    qty = int(request.POST.get('qty'))

    product.quantity_in_stock += qty
    product.save()

    StockMovement.objects.create(
        product=product,
        qty=qty,
        movement_type = 'EXPORT',
        note = "Xuất kho",

    )
    return redirect('')