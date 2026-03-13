from django.db import models


from category.models import Category




# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    import_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sku:
            category_code = self.category.code

            from product.services.make_new_sku import generate_sku
            self.sku = generate_sku(category_code)

        super().save(*args, **kwargs)