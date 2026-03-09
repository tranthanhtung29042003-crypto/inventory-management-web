from django.contrib.auth import get_user_model

import user.services

User = get_user_model()


def add_user(request_user, username, email, password, phone, role):

    # 1️⃣ Check permission
    check_role_user(request_user, role)

    # 2️⃣ Validate data
    validate_user_data(username, email, password, phone)

    # 3️⃣ Check email exists
    check_exist_email(email)

    # 4️⃣ Create user (password auto hash)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    user.phone = phone
    user.role = role
    user.save()

    return user