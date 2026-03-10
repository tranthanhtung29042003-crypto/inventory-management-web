
from django.urls import path
from .views import login_view, dashboard, logout_view, listuserview, listloguser, edit_user, delete_user, add_new_user

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/",dashboard, name = "dashboard"),

    path("listuserview", listuserview, name = "listuserview"),
    path("listloguser", listloguser, name = "listloguser"),
    path("user/edit-user/<int:id>/", edit_user, name="user/edit_user"),
    path("user/add-user", add_new_user, name="user/add_user"),
    path("user/delete-user/<int:id>/", delete_user, name="user/delete_user"),
]