from django.contrib import admin

# Register your models here.
from .models import Receipt, Item, Product, Category, ItemNameProduct


admin.site.register([Receipt, Item])


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("categories",)  # nicer UI for categories


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ItemNameProduct)
class ItemNameProductAdmin(admin.ModelAdmin):
    list_display = ("item_name", "product")
    search_fields = ("item_name", "product__name")
