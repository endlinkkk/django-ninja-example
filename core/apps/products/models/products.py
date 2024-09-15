from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.products.entities.products import Product as ProductEntity


class Product(TimeBaseModel):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара", blank=True)
    is_active = models.BooleanField(
        default=True, verbose_name="Видимость товара в каталоге"
    )

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            oid=self.pk,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
