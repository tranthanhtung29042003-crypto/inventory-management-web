
from django.urls import path

from .views import activity_list

urlpatterns = [


    path("listactivitylog", activity_list, name = "listactivitylog"),


]