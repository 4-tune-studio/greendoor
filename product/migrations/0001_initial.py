# Generated by Django 4.0 on 2022-03-28 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("meta_description", models.TextField(blank=True)),
                ("slug", models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("slug", models.SlugField(allow_unicode=True, default="", max_length=200, unique=True)),
                ("image", models.ImageField(blank=True, upload_to="products/%Y/%m/%d")),
                ("description", models.TextField(blank=True)),
                ("meta_description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("available_display", models.BooleanField(default=True, verbose_name="Display")),
                ("available_order", models.BooleanField(default=True, verbose_name="Order")),
                ("size", models.IntegerField(blank=True, null=True)),
                ("info", models.CharField(blank=True, max_length=500, null=True)),
                ("image_tag", models.TextField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "index_together": {("id", "slug")},
            },
        ),
    ]
