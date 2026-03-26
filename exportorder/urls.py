
from django.urls import path
from .views import create_export_order, export_order_list ,export_pdf, detail_export_order, delete_export_order

urlpatterns = [
    path("create/", create_export_order, name="create_export_order"),
    path('list/', export_order_list, name="export_order_list"),
    path('detailorder/<str:code>', detail_export_order, name="detail_export_order"),
    path('detailorder/<str:code>/export_pdf', export_pdf, name="export_pdf"),
    path('deleteorder/<str:code>',delete_export_order, name="delete_export_order"),
]