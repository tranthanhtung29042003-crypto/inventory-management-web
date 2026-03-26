from django.db.models import Sum
from django.shortcuts import render

from category.models import Category

from activitylog.models import ActivityLog
from exportorder.models import ExportOrder
from importorder.models import ImportOrder
from product.models import Product


# Create your views here.
def dashboard(request):

    total_product = Product.objects.count()
    total_category = Category.objects.count()

    total_import = ImportOrder.objects.count()
    total_export = ExportOrder.objects.count()

    total_import_amount = ImportOrder.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    total_export_amount = ExportOrder.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    total_stock = Product.objects.aggregate(
        total=Sum("quantity_in_stock")
    )["total"] or 0


    category_data = Category.objects.annotate(
        total_stock=Sum("product__quantity_in_stock")
    )


    top_products = Product.objects.order_by("-quantity_in_stock")[:5]

    # ====== activity ======
    logs = ActivityLog.objects.select_related("user").order_by("-created_at")[:5]

    context = {
        "total_product": total_product,
        "total_category": total_category,
        "total_import": total_import,
        "total_export": total_export,
        "total_import_amount": total_import_amount,
        "total_export_amount": total_export_amount,
        "total_stock": total_stock,
        "category_data": category_data,
        "top_products": top_products,
        "logs": logs,
    }

    return render(request, "dashboard.html", context)