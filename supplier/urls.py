


from django.urls import path
from .views import supplier_page, delete_supplier, update_supplier

urlpatterns = [
    path("supplier_page/", supplier_page, name="supplier_page"),
    path("delete_supplier/<int:id>/", delete_supplier, name="delete_supplier"),
    path("update_supplier/<int:id>/", update_supplier, name="update_supplier"),

]