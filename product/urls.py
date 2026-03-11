from django.contrib.auth import views
from django.urls import path

from .views import product_list, add_product, update_product, delete_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path("add_product/", add_product, name='add_product'),
    path("update_product/<int:id>", update_product, name='update_product'),
    path("delete_product", delete_product, name='delete_product'),
]