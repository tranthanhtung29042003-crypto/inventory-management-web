from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import render

from .models import ActivityLog

from exportorder.models import ExportOrder

from category.models import Category
from importorder.models import ImportOrder
from product.models import Product

from .utils.current_user import get_current_user


def activity_list(request):
    logs = ActivityLog.objects.select_related("user").order_by("-created_at")
    print(logs)
    return render(request, "activity/list.html", {
        "logs": logs
    })



@receiver(post_save, sender= Category)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="CREATE" if created else "UPDATE",
        model_name="Category",
        object_id=instance.id,
        description=f"{'Tạo' if created else 'Sửa'} đơn {instance.id}"
    )

@receiver(post_delete, sender=Category)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="DELETE",
        model_name="Category",
        object_id=instance.id,
        description=f"Xóa đơn {instance.id}"
    )




@receiver(post_save, sender= Product)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="CREATE" if created else "UPDATE",
        model_name="Product",
        object_id=instance.id,
        description=f"{'Tạo' if created else 'Sửa'} đơn {instance.sku}"
    )

@receiver(post_delete, sender=Product)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="DELETE",
        model_name="Product",
        object_id=instance.id,
        description=f"Xóa đơn {instance.sku}"
    )



@receiver(post_save, sender=ImportOrder)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="CREATE" if created else "UPDATE",
        model_name="ExportOrder",
        object_id=instance.id,
        description=f"{'Tạo' if created else 'Sửa'} đơn {instance.code}"
    )

@receiver(post_delete, sender=ImportOrder)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="DELETE",
        model_name="ExportOrder",
        object_id=instance.id,
        description=f"Xóa đơn {instance.code}"
    )


@receiver(post_save, sender=ExportOrder)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="CREATE" if created else "UPDATE",
        model_name="ExportOrder",
        object_id=instance.id,
        description=f"{'Tạo' if created else 'Sửa'} đơn {instance.code}"
    )

@receiver(post_delete, sender=ExportOrder)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    ActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action="DELETE",
        model_name="ExportOrder",
        object_id=instance.id,
        description=f"Xóa đơn {instance.code}"
    )