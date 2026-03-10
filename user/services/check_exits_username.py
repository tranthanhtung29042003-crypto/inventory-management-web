from django.contrib.auth import get_user_model

User = get_user_model()


def check_exist_username(username):
    if User.objects.filter(email=username).exists():
        raise ValueError("Email already exists")