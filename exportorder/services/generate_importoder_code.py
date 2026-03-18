from datetime import datetime
from django.apps import apps


def generate_exportoder_code():

    ExportOrder = apps.get_model('exportorder', 'ExportOrder')

    today = datetime.now().strftime("%Y%m%d")

    count = ExportOrder.objects.filter(
        code__startswith=f"EXP-{today}"
    ).count() + 1

    return f"EXP-{today}-{count:03d}"