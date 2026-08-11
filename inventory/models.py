from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=5)  # Alerta para el visor 3D
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='URL de imagen libre de derechos (Unsplash, Pexels, etc.)',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self) -> bool:
        return self.current_stock <= self.min_stock


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='movements'
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    # Nuevo campo para Razón Social / Cliente / Proveedor
    entity_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Razón Social / Proveedor / Cliente',
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movement_type} - {self.product.name} ({self.quantity})'

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if not self.pk:
            prod = self.product
            if self.movement_type == "IN":
                prod.current_stock += self.quantity
            elif self.movement_type == "OUT":
                if prod.current_stock < self.quantity:
                    raise ValueError("Stock insuficiente.")
                prod.current_stock -= self.quantity
            elif self.movement_type == "ADJ":
                prod.current_stock = self.quantity

            prod.save()

        super().save(*args, **kwargs)
