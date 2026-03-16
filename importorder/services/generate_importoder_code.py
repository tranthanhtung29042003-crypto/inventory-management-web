from datetime import datetime
from django.apps import apps


def generate_importoder_code():

    ImportOrder = apps.get_model('importorder', 'ImportOrder')

    today = datetime.now().strftime("%Y%m%d")

    count = ImportOrder.objects.filter(
        code__startswith=f"IMP-{today}"
    ).count() + 1

    return f"IMP-{today}-{count:03d}"