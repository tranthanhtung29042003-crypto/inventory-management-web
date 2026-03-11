from datetime import datetime

from product.models import Product


def generate_sku(category_code):

    today = datetime.now().strftime("%Y%m%d")

    count = Product.objects.filter(
        sku__startswith=f"{category_code}-{today}"
    ).count() + 1

    return f"{category_code}-{today}-{count:04d}"