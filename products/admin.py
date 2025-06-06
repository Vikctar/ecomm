from django.contrib import admin

from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'get_full_path', 'product_count', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def get_full_path(self, obj):
        return obj.get_full_path()

    get_full_path.short_description = 'Full Path'

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'categories', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['categories']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')

