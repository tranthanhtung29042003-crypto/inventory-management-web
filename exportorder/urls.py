
from django.urls import path
from .views import create_export_order, export_order_list ,export_pdf, detail_export_order, delete_export_order

urlpatterns = [
    path("create/", create_export_order, name="create_export_order"),
    path('list/', export_order_list, name="export_order_list"),
    path('detailorder/<int:id>', detail_export_order, name="detail_export_order"),
    path('detailorder/<int:id>/export_pdf', export_pdf, name="export_pdf"),
    path('deleteorder/<int:id>',delete_export_order, name="delete_export_order"),
]