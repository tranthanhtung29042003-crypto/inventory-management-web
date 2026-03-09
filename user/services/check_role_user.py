from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()


def check_role_create_user(request_user, new_role):

    # Chỉ Admin và Manager được tạo user
    if request_user.role not in [User.Role.ADMIN, User.Role.MANAGER]:
        raise PermissionDenied("You do not have permission to create user")

    # Manager không được tạo Admin
    if request_user.role == User.Role.MANAGER and new_role == User.Role.ADMIN:
        raise PermissionDenied("Manager cannot create Admin")