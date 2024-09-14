# Generated by Django 5.1.1 on 2024-09-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название товара"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Описание товара"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Видимость товара в каталоге"
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
    ]