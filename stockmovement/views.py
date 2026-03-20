from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from product.models import Product
from stockmovement.models import StockMovement


# Create your views here.

def stock_history(request):
    histories = StockMovement.objects.select_related('product').order_by('-created_at')
    return render(request, 'stock_history/stock_history.html', {'histories': histories})


def import_product(request, id):
    product = get_object_or_404(Product, id=id)
    qty = int(request.POST.get('qty', 0))

    handle_stock(product, qty, 'IMPORT')

    return redirect('product_detail', id=id)

def export_product(request, id):
    product = get_object_or_404(Product, id=id)
    qty = int(request.POST.get('qty', 0))

    try:
        handle_stock(product, qty, 'EXPORT')
    except ValueError:
        return render(request, 'error.html', {
            'message': 'Không đủ hàng'
        })

    return redirect('product_detail', id=id)

def handle_stock(product, qty, movement_type):
    with transaction.atomic():

        if movement_type == 'IMPORT':
            product.quantity_in_stock += qty

        elif movement_type == 'EXPORT':
            if product.quantity_in_stock < qty:
                raise ValueError("Không đủ tồn kho")
            product.quantity_in_stock -= qty

        product.save()

        StockMovement.objects.create(
            product=product,
            qty=qty,
            movement_type=movement_type
        )