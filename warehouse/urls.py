
from django.urls import path
from .views import warehouse_page, delete_warehouse, update_warehouse

urlpatterns = [
    path("", warehouse_page, name="warehouse_page"),
    path("delete_warehouse/<int:id>/", delete_warehouse, name="delete_warehouse"),
    path("update_supplier/<int:id>/", update_warehouse, name="update_warehouse"),

]