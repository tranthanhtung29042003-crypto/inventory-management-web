from django.contrib.auth import views
from django.urls import path

from .views import stock_history

urlpatterns = [
    path('', stock_history, name='stock_history'),

]