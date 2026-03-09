from django.contrib.auth import get_user_model

User = get_user_model()


def check_exist_email(email):
    if User.objects.filter(email=email).exists():
        raise ValueError("Email already exists")