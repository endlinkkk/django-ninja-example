from django.db import models

from core.apps.common.models import TimeBaseModel


class Product(TimeBaseModel):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара", blank=True)
    is_active = models.BooleanField(
        default=True, verbose_name="Видимость товара в каталоге"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title
