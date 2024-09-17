# Generated by Django 5.1.1 on 2024-09-17 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_token'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('rating', models.PositiveSmallIntegerField(default=1, verbose_name='User rating')),
                ('text', models.TextField(blank=True, default='', verbose_name='Review text')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='customers.customer', verbose_name='Reviewer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product review',
                'verbose_name_plural': 'Product reviews',
                'unique_together': {('customer', 'product')},
            },
        ),
    ]
