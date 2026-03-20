from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import ExportOrderForm
from .models import ExportOrder
import os
from exportorderitem.models  import ExportOrderItem
from .forms import ExportOrderItemFormSet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path = os.path.join(settings.BASE_DIR, 'assets/fonts/Roboto/Roboto-Regular.ttf')


pdfmetrics.registerFont(TTFont('Roboto', font_path))

def create_export_order(request):
    form = ExportOrderForm(request.POST or None)
    formset = ExportOrderItemFormSet(
        request.POST or None,
        queryset=ExportOrderItem.objects.none()
    )

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():

            order = form.save(commit=False)
            order.created_by = request.user

            total = 0


            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    quantity = f.cleaned_data.get('quantity')
                    price = f.cleaned_data.get('unit_price')

                    total += quantity * price


            order.total_amount = total
            order.save()


            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    item = f.save(commit=False)
                    item.export_order = order

                    product = item.product
                    product.quantity_in_stock -= item.quantity
                    product.save()

                    item.save()

            return redirect('export_order_list')

    return render(request, 'export_order/create_export_order.html', {
        'form': form,
        'formset': formset
    })

def export_order_list(request):

    search = request.GET.get("search")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    export_orders = ExportOrder.objects.select_related(

        "created_by"
    )

    if search:
        export_orders = export_orders.filter(
            code__icontains=search
        )

    if from_date:
        export_orders = export_orders.filter(
            created_at__date__gte=from_date
        )

    if to_date:
        export_orders = export_orders.filter(
            created_at__date__lte=to_date
        )

    export_orders = export_orders.order_by("-created_at")

    return render(request, "export_order/list_export_order.html", {
        "export_orders": export_orders
    })


def detail_export_order(request, id):
    order = get_object_or_404(
        ExportOrder.objects.select_related(
               "created_by"
        ).prefetch_related("items"),
        id=id
    )

    return render(request, "export_order/detail_export_order.html", {
        "order": order
    })

def delete_export_order(request, id):
    order = get_object_or_404(ExportOrder.objects.select_related(

            "created_by"
        ).prefetch_related("items"),
        id=id)
    order.delete()
    return redirect("exportorder_list")


def export_pdf(request, id):
    order = get_object_or_404(ExportOrder, id=id)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{order.code}.pdf"'

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

    elements.append(Paragraph("PHIẾU XUẤT KHO", styles['Title']),)
    elements.append(Spacer(1, 10))


    # Info
    elements.append(Paragraph(f"Mã phiếu: {order.code}", styles['Normal']))
    elements.append(Paragraph(f"Khách hàng: {order.customer_name}", styles['Normal']))
    elements.append(Paragraph(f"Ghi chú: {order.note}", styles['Normal']))




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