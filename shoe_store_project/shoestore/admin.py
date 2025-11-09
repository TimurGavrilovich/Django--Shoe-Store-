from django.contrib import admin
from shoestore.models import Category, Brand, Product, ProductSize, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'in_stock', 'featured']
    list_filter = ['category', 'brand', 'gender', 'featured', 'in_stock']
    list_editable = ['price', 'in_stock', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]

admin.site.register(Cart)
admin.site.register(CartItem)