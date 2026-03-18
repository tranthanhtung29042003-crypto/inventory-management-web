
from django.urls import path
from .views import create_import_order, import_order_list,export_pdf, detail_import_order, delete_import_order

urlpatterns = [
    path("create/", create_import_order, name="create_import_order"),
    path('list/', import_order_list, name="importorder_list"),
    path('detailorder/<int:id>', detail_import_order, name="detail_import_order"),
    path('detailorder/<int:id>/export_pdf', export_pdf, name="export_pdf"),
    path('deleteorder/<int:id>',delete_import_order, name="delete_import_order"),
]