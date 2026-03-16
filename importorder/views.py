from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImportOrderForm
from .models import ImportOrder
from importorderitem.models  import ImportOrderItem
from .forms import ImportOrderItemFormSet


def create_import_order(request):

    if request.method == "POST":

        form = ImportOrderForm(request.POST, request.FILES)
        formset = ImportOrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            import_order = form.save(commit=False)
            import_order.created_by = request.user
            import_order.save()

            items = formset.save(commit=False)

            for item in items:
                item.import_order = import_order
                item.save()

            return redirect("importorder_list")

    else:
        form = ImportOrderForm()
        formset = ImportOrderItemFormSet(queryset=ImportOrderItem.objects.none())

    return render(request, "import_order/create_import_order.html", {
        "form": form,
        "formset": formset
    })

def import_order_list(request):

    search = request.GET.get("search")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    import_orders = ImportOrder.objects.select_related(
        "supplier",
        "created_by"
    )

    if search:
        import_orders = import_orders.filter(
            code__icontains=search
        )

    if from_date:
        import_orders = import_orders.filter(
            created_at__date__gte=from_date
        )

    if to_date:
        import_orders = import_orders.filter(
            created_at__date__lte=to_date
        )

    import_orders = import_orders.order_by("-created_at")

    return render(request, "import_order/list_import_order.html", {
        "import_orders": import_orders
    })


def detail_import_order(request, id):
    order = get_object_or_404(
        ImportOrder.objects.select_related(
            "supplier",
            "created_by"
        ).prefetch_related("items"),
        id=id
    )

    return render(request, "import_order/detail_import_order.html", {
        "order": order
    })

def delete_import_order(request, id):
    order = get_object_or_404(ImportOrder.objects.select_related(
            "supplier",
            "created_by"
        ).prefetch_related("items"),
        id=id)
    order.delete()
    return redirect("importorder_list")