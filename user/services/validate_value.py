import re


def validate_user_data(username, email, password, phone):

    if not username or not email or not password:
        raise ValueError("Username, email and password are required")

    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")

    if not phone.isdigit():
        raise ValueError("Phone must contain only numbers")