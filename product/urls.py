from django.contrib.auth import views
from django.urls import path

from .views import product_list, add_product, update_product, delete_product, export_product_excel

urlpatterns = [
    path('', product_list, name='product_list'),
    path("add_product/", add_product, name='add_product'),
    path("export_product_excel/", export_product_excel, name='export_product_excel'),

    path("update_product/<int:id>", update_product, name='update_product'),
    path("delete_product/<int:id>", delete_product, name='delete_product'),
]