from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import ImportOrderForm
from .models import ImportOrder
import os
from importorderitem.models  import ImportOrderItem
from .forms import ImportOrderItemFormSet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from product.models import Product
from stockmovement.models import StockMovement

font_path = os.path.join(settings.BASE_DIR, 'assets/fonts/Roboto/Roboto-Regular.ttf')


pdfmetrics.registerFont(TTFont('Roboto', font_path))

def create_import_order(request):

    if request.method == "POST":

        form = ImportOrderForm(request.POST, request.FILES)
        formset = ImportOrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            try:
                with transaction.atomic():

                    import_order = form.save(commit=False)
                    import_order.created_by = request.user
                    import_order.save()

                    total_amount = 0

                    warehouse = import_order.warehouse

                    items = formset.save(commit=False)

                    for item in items:
                        item.import_order = import_order
                        item.save()

                        total_amount += item.quantity * item.price

                        pw, created = Product.objects.get_or_create(
                            product=item.product,
                            warehouse=warehouse,
                            defaults={"quantity":0}
                        )
                        pw.quantity_in_stock += item.quantity
                        pw.save()

                        StockMovement.objects.create(
                            product=item.product,
                            warehouse=  warehouse,
                            quantity=item.quantity,
                            type="IMPORT"
                        )

                        import_order.total_amount += total_amount
                        import_order.save()

                        for obj in formset.deleted_forms:
                            obj.delete()



                    return redirect("importorder_list")
            except Exception as e:
                print(e)
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


def export_pdf(request, id):
    order = get_object_or_404(ImportOrder, id=id)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="import_order_{order.id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1, fontName='Roboto'))
    styles.add(ParagraphStyle(name='Right', alignment=2, fontName='Roboto'))
    styles.add(ParagraphStyle(name='Bold', fontName='Roboto-Bold'))

    styles.add(ParagraphStyle(name="Small", fontName="Roboto", fontSize=9, leading=12))
    for style_name in styles.byName:
        styles[style_name].fontName = 'Roboto'
    elements = []

    # Title
    elements.append(Paragraph("CÔNG TY ABC", ParagraphStyle(name='header', fontName='Roboto', alignment=2)))
    elements.append(Paragraph("Địa chỉ: TP.HCM | SĐT: 0123456789", ParagraphStyle(name='header', fontName='Roboto', alignment=2)))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("PHIẾU NHẬP KHO", styles['Title']),)
    elements.append(Spacer(1, 10))


    # Info
    elements.append(Paragraph(f"Mã phiếu: {order.code}", styles['Normal']))
    elements.append(Paragraph(f"Nhà cung cấp: {order.supplier.name}", styles['Normal']))
    elements.append(Paragraph(f"Ngày: {order.created_at.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # Table data
    data = [
        ["STT", f"Sản phẩm", f"Số lượng", f"Đơn giá", f"Thành tiền"]
    ]

    for i, item in enumerate(order.items.all(), start=1):
        data.append([
            i,
            item.product.name,
            item.quantity,
            item.unit_price,
            item.quantity * item.unit_price
        ])

    # Table
    table = Table(data, colWidths=[60 , 100 ])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, -1), "Roboto", 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 2))

    # Total
    elements.append(Paragraph(
        f"Tổng tiền: {order.total_amount:,} VNĐ",
        ParagraphStyle(name='total', fontName='Roboto', alignment=2, fontSize=12)
    ))
    elements.append(Spacer(1, 30))

    sign_data = [
        ["Người lập", "Thủ kho", "Giám đốc"],

        ["(Ký, họ tên)", "(Ký, họ tên)", "(Ký, đóng dấu)"]
    ]

    sign_table = Table(sign_data,
                       colWidths=[180, 180, 180],
                       rowHeights=[20, 100]
                       )

    sign_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 1), (-1, 1), 30),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ("FONT", (0, 0), (-1, -1), "Roboto", 10),
    ]))

    elements.append(sign_table)

    doc.build(elements)

    return response