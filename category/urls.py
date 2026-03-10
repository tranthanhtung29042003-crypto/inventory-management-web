
from django.urls import path
from .views import listcagegoryview, delete_category, add_category

urlpatterns = [


    path("listcategory", listcagegoryview, name = "listcategoryview"),

    path("category/add-category", add_category, name="category/add_category"),
    path("category/delete-category/<int:id>/", delete_category, name="category/delete_category"),
]