
from django.urls import path
from .views import login_view, dashboard, logout_view, listuserview, listloguser

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/",dashboard, name = "dashboard"),

    path("listuserview", listuserview, name = "listuserview"),
    path("listloguser", listloguser, name = "listloguser")
]